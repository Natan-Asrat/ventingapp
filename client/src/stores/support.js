import { defineStore } from 'pinia';
import { ref } from 'vue';
import api from "@/api/axios"

export const useSupportStore = defineStore('support', () => {
  const isOpen = ref(false);
  const open = () => {
      isOpen.value = true;
  }
  const close = () => {
      isOpen.value = false;
  }
  const fetchContacts = async () => {
    const response = await api.get('/support/contacts/');
    return response;
  }
  return {
    isOpen,
    open,
    close,
    fetchContacts
  }
});