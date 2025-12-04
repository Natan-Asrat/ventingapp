def optimize_report_queryset(qs):
    return qs.select_related(
        "reported_post",
        "reported_post__posted_by",

        "reported_transaction",

        "reported_message__user", 
        "reported_message__reply_to", 
        "reported_message__reply_to__user", 
        "reported_message__shared_post", 
        "reported_message__shared_post__posted_by",
        "reported_message__reply_to__forwarded_from",
        "reported_message__reply_to__forwarded_from__user",
        "reported_message__reply_to__shared_post",
        "reported_message__reply_to__shared_post__posted_by",
        "reported_message__forwarded_from",
        "reported_message__forwarded_from__user",
        "reported_message__forwarded_from__shared_post",
        "reported_message__forwarded_from__shared_post__posted_by",
    ).prefetch_related(
        "decisions",

        "reported_post__payment_info_list",

        "reported_message__shared_post__payment_info_list",
        "reported_message__reply_to__shared_post__payment_info_list",
        "reported_message__forwarded_from__shared_post__payment_info_list"
    )
