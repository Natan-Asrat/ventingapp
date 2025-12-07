import { defineStore } from 'pinia';
import api from "@/api/axios" 

export const useCommentStore = defineStore('comment', () => {
    const likeComment = async (comment_id, liked) => {
        const endpoint = liked 
            ? `/post/comments/${comment_id}/unlike_comment/`
            : `/post/comments/${comment_id}/like_comment/`;
            
        const response = await api.post(endpoint);
        return response;
    }

    const replyComment = async (comment_id, message) => {
        const response = await api.post(`/post/comments/${comment_id}/reply/`, {
            message: message.trim()
        });
        return response;
    }

    const getReplies = async (comment_id) => {
        const response = await api.get(`/post/comments/${comment_id}/replies/`);
        return response;
    }

    return {
        likeComment,
        replyComment,
        getReplies
    }
})