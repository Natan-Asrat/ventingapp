<template>
    <div class="relative">
        <div ref="descriptionContainer" class="relative">
          <p 
            ref="descriptionRef"
            class="text-gray-800 whitespace-pre-line transition-all duration-200"
            :class="!isExpanded && 'line-clamp-2'"
          >
            {{ text }}
          </p>
          <span 
            v-if="showReadMore"
            @click="toggleDescription"
            class="text-sm text-indigo-600 hover:text-indigo-800 cursor-pointer ml-1 absolute bottom-0 right-0 bg-white pl-1"
            :class="{ 'relative': isExpanded }"
          >
            {{ isExpanded ? 'Show less' : 'Read more' }}
          </span>
        </div>
    </div>
</template>
<script setup>
import { ref, onMounted, watch, nextTick, onUnmounted } from 'vue';
const props = defineProps({
    text: String
})


const isExpanded = ref(false);
const descriptionRef = ref(null);
const descriptionContainer = ref(null);
const showReadMore = ref(false);

// Check if the description is long enough to need a "Read more" button
const checkIfClamped = () => {
  if (!descriptionRef.value) return;
  
  // Reset line-clamp to check the full height
  descriptionRef.value.style.webkitLineClamp = 'unset';
  
  // Get the full height of the content
  const fullHeight = descriptionRef.value.scrollHeight;
  
  // Set line-clamp back to 2 to check if it's being truncated
  descriptionRef.value.style.webkitLineClamp = '2';
  
  // Check if the content is being truncated
  const isClamped = fullHeight > descriptionRef.value.clientHeight;
  
  // Only update if the state has changed to prevent unnecessary re-renders
  if (showReadMore.value !== isClamped) {
    showReadMore.value = isClamped;
  }
};

const toggleDescription = (e) => {
  e.stopPropagation();
  isExpanded.value = !isExpanded.value;
};

// Check on component mount and when post description changes
onMounted(() => {
  // Use nextTick to ensure the DOM is updated
  nextTick(() => {
    checkIfClamped();
    // Also check when the window is resized
    window.addEventListener('resize', checkIfClamped);
  });
});

// Clean up event listener
onUnmounted(() => {
  window.removeEventListener('resize', checkIfClamped);
});

// Watch for changes in the post description
watch(() => props.text, () => {
  nextTick(() => {
    checkIfClamped();
  });
});

</script>
