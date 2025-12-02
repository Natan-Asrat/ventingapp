<template>
  <div class="relative inline-block text-left">
    <div>
      <button
        type="button"
        class="flex items-center text-gray-500 hover:text-gray-700 focus:outline-none"
        @click.stop="toggleMenu"
      >
        <slot name="trigger">
          <EllipsisVertical class="h-5 w-5" />
        </slot>
      </button>
    </div>

    <transition
      enter-active-class="transition ease-out duration-100"
      enter-from-class="transform opacity-0 scale-95"
      enter-to-class="transform opacity-100 scale-100"
      leave-active-class="transition ease-in duration-75"
      leave-from-class="transform opacity-100 scale-100"
      leave-to-class="transform opacity-0 scale-95"
    >
      <div
        v-if="isOpen"
        class="fixed z-50 mt-2 w-48 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
        :style="{
          top: `${menuPosition.top}px`,
          right: `${menuPosition.right}px`
        }"
        role="menu"
        aria-orientation="vertical"
        tabindex="-1"
        v-click-outside="closeMenu"
        ref="menu"
      >
        <div class="py-1" role="none">
          <slot></slot>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { EllipsisVertical } from 'lucide-vue-next';

const props = defineProps({
  closeOnClick: {
    type: Boolean,
    default: true
  }
});

const emit = defineEmits(['open', 'close']);

const isOpen = ref(false);
const menu = ref(null);
const menuPosition = ref({ top: 0, right: 0 });

const calculateMenuPosition = (event) => {
  if (!event) return;
  
  const buttonRect = event.target.getBoundingClientRect();
  const viewportHeight = window.innerHeight;
  
  // Position below the button by default
  let top = buttonRect.bottom + window.scrollY;
  
  // If there's not enough space below, position above the button
  if (top + 200 > viewportHeight) {
    top = buttonRect.top + window.scrollY - 200; // Assuming max height of 200px
  }
  
  menuPosition.value = {
    top: top,
    right: window.innerWidth - buttonRect.right
  };
};

const toggleMenu = (event) => {
  if (!isOpen.value) {
    calculateMenuPosition(event);
  }
  isOpen.value = !isOpen.value;
  if (isOpen.value) {
    emit('open');
  } else {
    emit('close');
  }
};

const closeMenu = () => {
  if (isOpen.value) {
    isOpen.value = false;
    emit('close');
  }
};

defineExpose({
  closeMenu
});
</script>
