import { defineStore } from 'pinia';

export const useSupportStore = defineStore('support', {
  state: () => ({
    isOpen: false,
  }),
  actions: {
    open() {
      this.isOpen = true;
    },
    close() {
      this.isOpen = false;
    },
  },
});