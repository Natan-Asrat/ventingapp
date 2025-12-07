import { defineStore } from "pinia";
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api/axios';

export const useNewPostStore = defineStore('newpost', () => {
    const router = useRouter();
    const createEmptyPost = () => ({
        description: '',
        image: null,
        payment_info: []
    });
    const post = ref(createEmptyPost());
    const isPaymentModalOpen = ref(false);

    const receiveDonations = ref(false);
    const imagePreview = ref(null);

    const newPaymentInfo = ref({
        method: '',
        account: '',
        nameOnAccount: ''
    });

    const setIsPaymentModalOpen = (value) => {
        isPaymentModalOpen.value = value;
    }
    const resetPost = () => {
        post.value = createEmptyPost();
        imagePreview.value = null;
    };
    const isLoading = ref(false);
    const setPostDescription = (value) => {
        post.value.description = value;
    }

    const setPostImage = (value) => {
        post.value.image = null;
    }

    const resetPaymentForm = () => {
        newPaymentInfo.value = {
            method: '',
            account: '',
            nameOnAccount: ''
        };
    };
    const addPaymentMethod = (paymentData) => {
        if (paymentData.method && paymentData.account) {
            post.value.payment_info.push({ ...paymentData });
            resetPaymentForm();
        }
    };

    const removePaymentMethod = (index) => {
        post.value.payment_info.splice(index, 1);
    };

    const setReceiveDonations = (value) => {
        receiveDonations.value = value;
    }

    const toggleReceiveDonations = () => {
        receiveDonations.value = !receiveDonations.value;
    }

    const setImagePreview = (value) => {
        imagePreview.value = value;
    }

    const handleImageUpload = (event) => {
        const file = event.target.files[0];
        if (!file) return;
        
        // Check file size (10MB max)
        if (file.size > 10 * 1024 * 1024) {
            alert('Image size should be less than 10MB');
            return;
        }
        
        // Check file type
        if (!file.type.match('image.*')) {
            alert('Please select an image file (JPEG, PNG, GIF)');
            return;
        }
    
        // Create preview
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.value = e.target.result;
        };
        reader.readAsDataURL(file);
        
        // Store the file
        post.value.image = file;
    };

    
    const submitPost = async () => {
        if (isLoading.value) return;
        
        try {
            isLoading.value = true;
            if(post.value.image != null){
                const formData = new FormData();
                formData.append('description', post.value.description);
                
                if (post.value.image) {
                    formData.append('image', post.value.image);
                }
                
                const response = await api.post('/post/posts/', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                        'Authorization': `Bearer ${localStorage.getItem('access_token')}` // Assuming you're using token-based auth
                    },
                });
                if (receiveDonations.value && post.value.payment_info?.length > 0) {
                    const payment_added_response = await api.post(`/post/posts/${response.data.id}/bulk_add_payment_info/`, post.value.payment_info, {
                        headers: {
                            'Content-Type': 'application/json',
                        },
                    });
                    console.log('Payment info added: ', payment_added_response.data)

                } else {
                    console.log('Post created:', response.data);

                }
                
                router.push('/home'); // Redirect to feed after successful post
            } else {
                const response = await api.post('/post/posts/', post.value, {
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });
                console.log('Post created:', response.data);
                router.push('/home'); // Redirect to feed after successful post
            }
        } catch (error) {
            console.error('Error creating post:', error);
            // You might want to show an error message to the user here
            if (error.response) {
            console.error('Error response:', error.response.data);
            }
        } finally {
            resetPost();
            isLoading.value = false;
        }
    };

    return {
        submitPost,
        setPostDescription,
        handleImageUpload,

        addPaymentMethod,
        removePaymentMethod,
        
        post,
        isLoading,
        receiveDonations,
        setReceiveDonations,
        toggleReceiveDonations,

        imagePreview,
        setImagePreview,
        setPostImage,
        newPaymentInfo,
        isPaymentModalOpen,
        
        setIsPaymentModalOpen
    }

})