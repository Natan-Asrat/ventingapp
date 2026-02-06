import json
import redis
import redis.exceptions
import time
import logging
from django.conf import settings
from .query import get_posts_queryset
from django.db.models import Q
from account.models import Connection

logger = logging.getLogger(__name__)

if settings.CACHE_ENABLED:
    try:
        redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
        redis_client.ping()
        try:
            # Set memory limit to 300MB
            redis_client.config_set('maxmemory', settings.REDIS_MAX_MEMORY)
            # Set eviction policy to delete least recently used keys when full
            redis_client.config_set('maxmemory-policy', settings.REDIS_MAX_MEMORY_POLICY)
            logger.info(f"[Redis] Successfully configured maxmemory {settings.REDIS_MAX_MEMORY} and {settings.REDIS_MAX_MEMORY_POLICY} policy.")
        except Exception as e:
            logger.error(f"[Redis] Failed to set config: {e}")
    except Exception as e:
        logger.error(f"[Redis] Failed to connect to Redis server: {e}")
        redis_client = None        
else:
    redis_client = None

def validate_and_assemble(post_ids, user):
    start = time.perf_counter()
    if not redis_client:
        return [], list(post_ids)

    # 1. STANDARDIZE: Ensure everything is an INT for local logic
    # and a STR for Redis keys.
    try:
        post_ids = [int(pid) for pid in post_ids]
        
        post_keys = [f"post:v1:{pid}" for pid in post_ids]
        raw_posts = redis_client.mget(post_keys)
        
        # Map raw results using INTEGER keys for the local dictionary
        posts_map = dict(zip(post_ids, raw_posts))
        
        missing_ids = set()
        posts_data = []
        author_map = {} # Key: Post ID (int), Value: Author ID (int)

        for pid, raw in posts_map.items():
            if not raw:
                missing_ids.add(pid)
                continue
            p_json = json.loads(raw)
            posts_data.append(p_json)
            # Force the author ID to int
            author_map[pid] = int(p_json['posted_by']['id'])

        if missing_ids:
            duration = (time.perf_counter() - start) * 1000
            logger.info(f"[Cache] Phase 1 missing IDs: {list(missing_ids)}. Time: {duration:.2f}ms")
            return [], list(missing_ids)

        # 2. Bitstrings
        # Get unique author IDs as integers
        unique_author_ids = list(set(author_map.values()))
        
        up_keys = [f"up:{user.id}:{pid}" for pid in post_ids]
        uu_keys = [f"uu:{user.id}:{aid}" for aid in unique_author_ids]
        
        # Fetch all at once
        raw_up_list = redis_client.mget(up_keys)
        raw_uu_list = redis_client.mget(uu_keys)
        
        # Map them back using integer keys
        up_map = dict(zip(post_ids, raw_up_list))
        uu_map = dict(zip(unique_author_ids, raw_uu_list))

        final_posts = []
        for p in posts_data:
            pid = int(p['id'])
            aid = int(p['posted_by']['id'])
            
            up_bit = up_map.get(pid)
            uu_bit = uu_map.get(aid)

            if not up_bit or not uu_bit:
                logger.warning(f"[Cache] Missing bitstrings for Post {pid} (UP: {bool(up_bit)}, UU: {bool(uu_bit)})")
                missing_ids.add(pid)
                continue

            up_parts = up_bit.decode().split('-')
            uu_parts = uu_bit.decode().split('-')
            
            p.update({
                'liked': up_parts[0] == '1',
                'saved': up_parts[1] == '1',
                'connected': uu_parts[0] == '1',
                'pending_connection': uu_parts[1] == '1',
                'rejected_connection': uu_parts[2] == '1',
                'banned_connection': uu_parts[3] == '1',
                'removed_connection': uu_parts[4] == '1',
            })
            final_posts.append(p)

        duration = (time.perf_counter() - start) * 1000
        logger.info(f"[Cache] validate_and_assemble took {duration:.2f}ms. Missing: {len(missing_ids)}")
        return final_posts, list(missing_ids)
    except redis.exceptions.RedisError as e:
        logger.error(f"[Cache] Redis error during assembly: {e}")
        return [], list(post_ids)

def get_cached_post_data(post_ids, user, depth=0):
    from .serializers import PostSimpleSerializer
    from .models import Post

    if not redis_client: 
        logger.error("[Cache] Redis client not initialized. Fallback to DB.")
        fallback_qs = Post.objects.filter(id__in=post_ids)
        return PostSimpleSerializer(get_posts_queryset(fallback_qs, user), many=True).data
    
    # Ensure all IDs are integers to prevent key mismatch
    post_ids = [int(pid) for pid in post_ids]

    if depth > 3:

        logger.error(f"[Cache] Max depth reached for IDs {post_ids}. Fallback to DB.")
        fallback_qs = Post.objects.filter(id__in=post_ids)
        return PostSimpleSerializer(get_posts_queryset(fallback_qs, user), many=True).data

    assembled, missing_ids = validate_and_assemble(post_ids, user)
    if not missing_ids:
        return assembled

    logger.info(f"[Cache] Depth {depth}: Recovering IDs {missing_ids} from DB")

    missing_qs = Post.objects.filter(id__in=missing_ids)
    recovered_qs = get_posts_queryset(missing_qs, user)
    
    start_write = time.perf_counter()
    # USE ONE PIPELINE FOR ALL POSTS
    pipe = redis_client.pipeline()
    from .serializers import PostSimpleSerializer

    
    for obj in recovered_qs:
        data = PostSimpleSerializer(obj).data
        # Force string key for Redis
        pid = str(obj.id)
        
        # Save Global Post
        pipe.set(f"post:v1:{pid}", json.dumps(data), ex=settings.REDIS_OBJECT_EXPIRY)
        
        # Save User-Post Bitstring
        up_bits = f"{'1' if obj.liked else '0'}-{'1' if obj.saved else '0'}"
        pipe.set(f"up:{user.id}:{pid}", up_bits, ex=settings.REDIS_OBJECT_EXPIRY)
        
        # Save User-User Bitstring
        aid = str(obj.posted_by_id)
        uu_bits = (f"{'1' if obj.connected else '0'}-{'1' if obj.pending_connection else '0'}-"
                   f"{'1' if obj.rejected_connection else '0'}-{'1' if obj.banned_connection else '0'}-"
                   f"{'1' if obj.removed_connection else '0'}")
        pipe.set(f"uu:{user.id}:{aid}", uu_bits, ex=settings.REDIS_OBJECT_EXPIRY)
    
    try:
        pipe.execute()
        write_time = (time.perf_counter() - start_write) * 1000
        logger.info(f"[Cache] Bulk Write to Redis took: {write_time:.2f}ms")
        return get_cached_post_data(post_ids, user, depth + 1)
    except redis.exceptions.RedisError as e:
        logger.error(f"[Cache] Pipeline execution failed: {e}")
        fallback_qs = Post.objects.filter(id__in=post_ids)
        return PostSimpleSerializer(get_posts_queryset(fallback_qs, user), many=True).data



def update_user_post_bitstring(user_id, post_id):
    """
    Fetches the current Liked/Saved status and updates the Redis bitstring.
    """
    if not settings.CACHE_ENABLED or not redis_client:
        return
    try:
        cache_key = f"up:{user_id}:{post_id}"
        
        # Check if the relation is already in Redis
        if not redis_client.exists(cache_key):
            logger.info(f"[Signal] {cache_key} not found in Redis. Skipping user-post update.")
            return # Skip: Self-healing will handle it on next feed load
        
        from .models import Like, Save

        is_liked = Like.objects.filter(post_id=post_id, liked_by_id=user_id, active=True).exists()
        is_saved = Save.objects.filter(post_id=post_id, saved_by_id=user_id, active=True).exists()

        new_val = f"{'1' if is_liked else '0'}-{'1' if is_saved else '0'}"
        redis_client.set(cache_key, new_val, ex=settings.REDIS_OBJECT_EXPIRY)
        logger.info(f"[Signal] Synced {cache_key} to {new_val}")
    except redis.exceptions.RedisError as e:
        logger.error(f"[Signal] Redis error updating bitstring: {e}")

def sync_connection_cache_by_ids(u1, u2):
    """
    Updates the UU bitstring using the most recently updated connection record.
    """
    if not settings.CACHE_ENABLED or not redis_client:
        return

    u1, u2 = int(u1), int(u2)
    
    # 1. Fetch the most recent connection record
    # We use .values() to pick exactly the fields we need for the bits
    conn = Connection.objects.filter(
        (Q(initiating_user_id=u1, connected_user_id=u2) | 
         Q(initiating_user_id=u2, connected_user_id=u1))
    ).order_by('-updated_at').values(
        'removed', 
        'reconnection_requested', 
        'reconnection_rejected', 
        'banned'
    ).first()

    # 2. Translate row data to bits
    if not conn:
        bits = "0-0-0-0-0"
    else:
        # Calculate flags based on your logic
        is_conn = not conn['removed']
        is_pending = (
            conn['reconnection_requested'] and 
            conn['removed'] and 
            not conn['reconnection_rejected']
        )
        is_rejected = conn['removed'] and conn['reconnection_rejected']
        is_banned = conn['banned']
        is_removed = conn['removed']

        bits = (
            f"{'1' if is_conn else '0'}-"
            f"{'1' if is_pending else '0'}-"
            f"{'1' if is_rejected else '0'}-"
            f"{'1' if is_banned else '0'}-"
            f"{'1' if is_removed else '0'}"
        )

    try:
        # 3. Bi-directional Redis update
        pipe = redis_client.pipeline()
        keys = [f"uu:{u1}:{u2}", f"uu:{u2}:{u1}"]
        
        for key in keys:
            if redis_client.exists(key):
                pipe.set(key, bits, ex=settings.REDIS_OBJECT_EXPIRY)
                
        pipe.execute()
        logger.info(f"[Cache Sync] UU {u1}<->{u2} | Most Recent Bits: {bits}")
    except redis.exceptions.RedisError as e:
        logger.error(f"[Cache Sync] UU sync failed: {e}")

def update_post_data(post_id):
    if not redis_client: return
    
    key = f"post:v1:{post_id}"
    # Purpose: post will not be updated unless the last time it was updated was at least a few seconds ago
    throttle_key = f"post:sync_lock:{post_id}"

    # 1. First check: is anyone even watching this post?
    if not redis_client.exists(key):
        return

    # 2. Second check: was this post updated in the last 1 seconds?
    # set(nx=True) only sets the key if it DOES NOT exist
    if not redis_client.set(throttle_key, "locked", ex=1, nx=True):
        logger.info(f"[Cache] Update skipped for {post_id} (Throttled)")
        return

    # Only update if someone is actually caching this post
    from .models import Post
    try:
        post_instance = Post.objects.get(id=post_id)
        # Use NoContextSerializer to keep the global cache "clean" 
        # (No liked/saved flags inside the global post JSON)
        from .serializers import PostNoContextSerializer

        post_data = PostNoContextSerializer(post_instance).data
        try:
            redis_client.set(key, json.dumps(post_data), ex=settings.REDIS_OBJECT_EXPIRY)
            logger.info(f"[Cache] Updated global post data for {post_id}")
        except redis.exceptions.RedisError as e:
            # If Redis fails, we just log it and move on. 
            # The app continues using the DB, and the user never sees an error.
            logger.error(f"[Cache] Failed to write to Redis for post {post_id}: {e}")
    except Post.DoesNotExist:
        try:
            redis_client.delete(key)
            # Also clear the throttle lock so a new post with same ID can be cached immediately
            redis_client.delete(throttle_key) 
        except redis.exceptions.RedisError:
            logger.error(f"[Cache] Failed to delete Redis keys for post {post_id}: {e}")
