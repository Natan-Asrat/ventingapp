<template>
  <div class="min-h-screen bg-gradient-to-b from-indigo-50 to-white">
    <!-- Navigation -->
    <nav class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex-shrink-0 flex items-center">
            <h1 class="text-xl font-bold text-indigo-600">VentingApp</h1>
          </div>
          <div class="flex items-center space-x-4">
            <router-link
              v-if="!isAuthenticated"
              to="/login"
              class="px-4 py-2 text-sm font-medium text-indigo-600 hover:text-indigo-800"
            >
              Sign in
            </router-link>
            <router-link
              v-if="!isAuthenticated"
              to="/signup"
              class="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700"
            >
              Get started
            </router-link>
            <router-link
              v-if="isAuthenticated"
              to="/home"
              class="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700"
            >
              Go to Home
            </router-link>
          </div>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div class="text-center">
        <h1 class="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
          <span class="block">Your Supportive Space to</span>
          <span class="block text-indigo-600">Share & Connect</span>
        </h1>
        <p class="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
          A dedicated platform to express yourself, share your daily experiences, and receive support from a caring community.
        </p>
        <div class="mt-5 max-w-md mx-auto sm:flex sm:justify-center md:mt-8">
          <div class="rounded-md shadow">
            <router-link
              to="/signup"
              class="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 md:py-4 md:text-lg md:px-10"
            >
              Join the Community
            </router-link>
          </div>
          <div class="mt-3 rounded-md shadow sm:mt-0 sm:ml-3">
            <a
              href="#features"
              class="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-indigo-600 bg-white hover:bg-gray-50 md:py-4 md:text-lg md:px-10"
            >
              Learn more
            </a>
          </div>
        </div>
      </div>

      <!-- Features Section -->
      <div id="features" class="mt-16">
        <h2 class="text-center text-3xl font-extrabold text-gray-900 sm:text-4xl">
          Why VentingApp?
        </h2>
        <div class="mt-12 grid gap-8 lg:grid-cols-3">
          <div class="pt-6">
            <div class="flow-root bg-white rounded-lg px-6 pb-8 h-full">
              <div class="-mt-6">
                <div class="flex items-center justify-center h-12 w-12 rounded-md bg-indigo-500 text-white">
                  <MessageSquare class="h-6 w-6" />
                </div>
                <h3 class="mt-8 text-lg font-medium text-gray-900 tracking-tight">Express Freely</h3>
                <p class="mt-5 text-base text-gray-500">
                  Share your thoughts and daily experiences in a supportive environment designed for meaningful connections.
                </p>
              </div>
            </div>
          </div>

          <div class="pt-6">
            <div class="flow-root bg-white rounded-lg px-6 pb-8 h-full">
              <div class="-mt-6">
                <div class="flex items-center justify-center h-12 w-12 rounded-md bg-indigo-500 text-white">
                  <Users class="h-6 w-6" />
                </div>
                <h3 class="mt-8 text-lg font-medium text-gray-900 tracking-tight">Earn Support</h3>
                <p class="mt-5 text-base text-gray-500">
                  Receive support through donations from the community who value your experiences and insights.
                </p>
              </div>
            </div>
          </div>

          <div class="pt-6">
            <div class="flow-root bg-white rounded-lg px-6 pb-8 h-full">
              <div class="-mt-6">
                <div class="flex items-center justify-center h-12 w-12 rounded-md bg-indigo-500 text-white">
                  <Send class=" h-5 w-5" />
                </div>
                <h3 class="mt-8 text-lg font-medium text-gray-900 tracking-tight">Track Engagement</h3>
                <p class="mt-5 text-base text-gray-500">
                  Gain insights into how your posts are performing with detailed analytics on views, likes, and comments.
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Additional Features -->
        <div class="mt-16">
          <div class="lg:grid lg:grid-cols-2 lg:gap-8 lg:items-center">
            <div class="mt-12 lg:mt-0">
              <h3 class="text-2xl font-extrabold text-gray-900">Connect with Others</h3>
              <p class="mt-3 text-lg text-gray-500">
                Build meaningful connections through private chats with other users who resonate with your experiences.
              </p>
              <div class="mt-8">
                <div class="flex items-start">
                  <div class="flex-shrink-0 flex items-center justify-center h-6 w-6 rounded-md bg-indigo-500 text-white">
                    <Check class="h-4 w-4" />
                  </div>
                  <p class="ml-3 text-base text-gray-700">Engage in private conversations with connections</p>
                </div>
                <div class="mt-4 flex items-start">
                  <div class="flex-shrink-0 flex items-center justify-center h-6 w-6 rounded-md bg-indigo-500 text-white">
                    <Check class="h-4 w-4" />
                  </div>
                  <p class="ml-3 text-base text-gray-700">Share your journey and support others</p>
                </div>
              </div>
            </div>
            <div class="mt-10 lg:mt-0">
              <div class="relative mx-auto w-full rounded-lg shadow-lg overflow-hidden">
                <div class="relative w-full flex items-center justify-center bg-gray-100 py-12 px-8">
                  <div class="w-full max-w-md">
                    <div class="bg-white rounded-lg shadow p-6">
                      <h4 class="text-lg font-medium text-gray-900">Join our community today</h4>
                      <p class="mt-2 text-sm text-gray-500">Start sharing your experiences and connect with others who understand.</p>
                      <div class="mt-6">
                        <router-link
                          to="/signup"
                          class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                        >
                          Create Account
                        </router-link>
                        <p class="mt-3 text-center text-sm text-gray-600">
                          Already have an account? <router-link to="/login" class="font-medium text-indigo-600 hover:text-indigo-500">
                            Sign in
                          </router-link>
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useUserStore } from '@/stores/user';
import { MessageSquare, Users, BarChart, Check, Send } from 'lucide-vue-next';

const userStore = useUserStore();
const isAuthenticated = computed(() => userStore.isAuthenticated);
</script>
