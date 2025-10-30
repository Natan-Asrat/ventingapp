<template>
  <TransitionRoot appear :show="modelValue" as="template">
    <Dialog as="div" class="fixed inset-0 z-50 overflow-y-auto" @close="close">
      <div class="min-h-screen px-4 text-center">
        <TransitionChild
          as="template"
          enter="ease-out duration-300"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="ease-in duration-200"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
          <DialogOverlay class="fixed inset-0 bg-black/75 transition-opacity" />
        </TransitionChild>

        <span class="inline-block h-screen align-middle" aria-hidden="true">
          &#8203;
        </span>

        <TransitionChild
          as="template"
          enter="ease-out duration-300"
          enter-from="opacity-0 scale-95"
          enter-to="opacity-100 scale-100"
          leave="ease-in duration-200"
          leave-from="opacity-100 scale-100"
          leave-to="opacity-0 scale-95"
        >
          <div 
            class="inline-block w-full max-w-4xl my-8 overflow-hidden text-left align-middle transition-all transform bg-transparent shadow-xl rounded-2xl"
            
          >
            <div class="relative">
              <img
                ref="imageViewer"
                :src="src"
                :alt="alt"
                class="w-full max-h-[80vh] object-contain cursor-zoom-out"
                :style="{
                  transform: `scale(${zoomLevel})`,
                  transformOrigin: `${transformOriginX}% ${transformOriginY}%`,
                  transition: zoomLevel === 1 ? 'transform 0.2s ease' : 'none'
                }"
                @wheel.prevent="handleWheel"
                @mousedown="startDrag"
                @mousemove="handleDrag"
                @mouseup="stopDrag"
                @mouseleave="stopDrag"
              />
              
              <!-- Close Button -->
              <button
                @click="close"
                class="absolute top-4 left-4 p-2 bg-black bg-opacity-50 rounded-full text-white hover:bg-opacity-75 transition-all focus:outline-none focus:ring-2 focus:ring-white cursor-pointer"
                title="Close (Esc)"
              >
                <X :size="24" />
              </button>
              
              <!-- Zoom Controls -->
              <div class="absolute bottom-4 right-4 flex flex-col space-y-2">
                <button
                  @click.stop="zoomIn"
                  class="p-2 bg-white bg-opacity-80 rounded-full shadow-md hover:bg-opacity-100 transition-all cursor-pointer"
                  title="Zoom In (Mouse Wheel Up)"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                </button>
                <button
                  @click.stop="zoomOut"
                  class="p-2 bg-white bg-opacity-80 rounded-full shadow-md hover:bg-opacity-100 transition-all cursor-pointer"
                  :class="{'opacity-50 cursor-not-allowed': zoomLevel <= 1}"
                  :disabled="zoomLevel <= 1"
                  title="Zoom Out (Mouse Wheel Down)"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4" />
                  </svg>
                </button>
                <button
                  @click.stop="resetZoom"
                  class="p-2 bg-white bg-opacity-80 rounded-full shadow-md hover:bg-opacity-100 transition-all cursor-pointer"
                  :class="{'opacity-50 cursor-not-allowed': zoomLevel === 1}"
                  :disabled="zoomLevel === 1"
                  title="Reset Zoom (R)"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                </button>
              </div>
              
              <!-- Zoom Level Indicator -->
              <div v-if="zoomLevel > 1" class="absolute bottom-4 left-1/2 transform -translate-x-1/2 px-3 py-1 bg-black bg-opacity-50 text-white text-sm rounded-full">
                {{ Math.round(zoomLevel * 100) }}%
              </div>
            </div>
          </div>
        </TransitionChild>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import { Dialog, TransitionRoot, TransitionChild, DialogOverlay } from '@headlessui/vue';
import { X } from 'lucide-vue-next';

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  src: {
    type: String,
    required: true
  },
  alt: {
    type: String,
    default: 'Image'
  }
});

const emit = defineEmits(['update:modelValue', 'close']);

const zoomLevel = ref(1);
const isDragging = ref(false);
const startX = ref(0);
const startY = ref(0);
const scrollLeft = ref(0);
const scrollTop = ref(0);
const transformOriginX = ref(50);
const transformOriginY = ref(50);

const close = () => {
  emit('update:modelValue', false);
  emit('close');
  resetZoom();
  document.body.style.overflow = '';
};

const zoomIn = () => {
  zoomLevel.value = Math.min(zoomLevel.value + 0.5, 5);
};

const zoomOut = () => {
  if (zoomLevel.value > 1) {
    zoomLevel.value = Math.max(zoomLevel.value - 0.5, 1);
  } else {
    close();
  }
};

const resetZoom = () => {
  zoomLevel.value = 1;
};

const handleWheel = (e) => {
  e.preventDefault();
  
  // Update transform origin based on mouse position
  const rect = e.target.getBoundingClientRect();
  const x = ((e.clientX - rect.left) / rect.width) * 100;
  const y = ((e.clientY - rect.top) / rect.height) * 100;
  
  transformOriginX.value = x;
  transformOriginY.value = y;
  
  // Zoom in/out based on wheel direction
  if (e.deltaY < 0) {
    zoomIn();
  } else {
    zoomOut();
  }
};

const startDrag = (e) => {
  if (zoomLevel.value <= 1) return;
  
  isDragging.value = true;
  startX.value = e.pageX - e.target.offsetLeft;
  startY.value = e.pageY - e.target.offsetTop;
  scrollLeft.value = e.target.scrollLeft;
  scrollTop.value = e.target.scrollTop;
  e.target.style.cursor = 'grabbing';
};

const handleDrag = (e) => {
  if (!isDragging.value || zoomLevel.value <= 1) return;
  e.preventDefault();
  
  const x = e.pageX - e.target.offsetLeft;
  const y = e.pageY - e.target.offsetTop;
  const walkX = (x - startX.value) * 1.5;
  const walkY = (y - startY.value) * 1.5;
  
  e.target.scrollLeft = scrollLeft.value - walkX;
  e.target.scrollTop = scrollTop.value - walkY;
};

const stopDrag = () => {
  isDragging.value = false;
  const image = document.querySelector('.cursor-zoom-out');
  if (image) {
    image.style.cursor = 'zoom-out';
  }
};

// Close modal on Escape key
const handleKeyDown = (e) => {
  if (e.key === 'Escape' && props.modelValue) {
    close();
  } else if (e.key === 'r' || e.key === 'R') {
    e.preventDefault();
    resetZoom();
  } else if (e.key === '+' || e.key === '=') {
    e.preventDefault();
    zoomIn();
  } else if (e.key === '-' || e.key === '_') {
    e.preventDefault();
    zoomOut();
  }
};

// Watch for modelValue changes to handle body scroll
watch(() => props.modelValue, (newVal) => {
  if (newVal) {
    document.body.style.overflow = 'hidden';
    window.addEventListener('keydown', handleKeyDown);
  } else {
    document.body.style.overflow = '';
    window.removeEventListener('keydown', handleKeyDown);
  }
});

onMounted(() => {
  if (props.modelValue) {
    document.body.style.overflow = 'hidden';
    window.addEventListener('keydown', handleKeyDown);
  }
});

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown);
  document.body.style.overflow = '';
});
</script>
