<template>
  <div class="min-h-screen bg-zinc-50 font-sans selection:bg-violet-100 selection:text-violet-900">
    <!-- Navigation -->
    <nav class="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md border-b border-zinc-100">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <!-- Logo -->
          <div class="flex-shrink-0 flex items-center gap-2 cursor-pointer" @click="scrollToTop">
             <div class="w-8 h-8 bg-violet-100 rounded-lg flex items-center justify-center text-violet-600 shadow-sm">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
             </div>
             <h1 class="text-xl font-bold text-zinc-900 tracking-tight">Venting<span class="text-violet-600">App</span></h1>
          </div>

          <!-- Desktop Nav Links -->
          <div class="hidden md:flex items-center space-x-8">
            <a href="#features" class="text-sm font-medium text-zinc-500 hover:text-violet-600 transition-colors">Features</a>
            <a href="#how-it-works" class="text-sm font-medium text-zinc-500 hover:text-violet-600 transition-colors">How it works</a>
          </div>

          <!-- Auth Buttons -->
          <div class="flex items-center space-x-3">
            <template v-if="!isAuthenticated">
              <router-link
                to="/login"
                class="hidden md:inline-flex px-4 py-2 text-sm font-medium text-zinc-600 hover:text-violet-600 transition-colors"
              >
                Sign in
              </router-link>
              <router-link
                to="/signup"
                class="inline-flex items-center justify-center px-5 py-2 text-sm font-semibold text-white bg-zinc-900 rounded-full hover:bg-violet-600 hover:shadow-lg hover:-translate-y-0.5 transition-all duration-300"
              >
                Get Started
              </router-link>
            </template>
            <template v-else>
               <router-link
                to="/home"
                class="inline-flex items-center justify-center px-5 py-2 text-sm font-semibold text-white bg-zinc-900 rounded-full hover:bg-violet-600 transition-all duration-300"
              >
                Go to App
              </router-link>
            </template>
          </div>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <main class="pt-32 pb-16 sm:pt-40 sm:pb-24 lg:pb-32 overflow-hidden">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
        <!-- Decorational blobs -->
        <div class="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-violet-200/20 rounded-full blur-3xl pointer-events-none"></div>
        
        <div class="text-center relative z-10 max-w-4xl mx-auto">
          <div class="inline-flex items-center px-3 py-1 rounded-full bg-violet-50 border border-violet-100 text-violet-600 text-xs font-bold uppercase tracking-wide mb-6">
            <span class="w-2 h-2 rounded-full bg-violet-600 mr-2 animate-pulse"></span>
            Join the conversation
          </div>
          
          <h1 class="text-5xl sm:text-6xl lg:text-7xl font-extrabold text-zinc-900 tracking-tight leading-tight mb-6">
            A safe space to <br class="hidden sm:block" />
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-violet-600 to-indigo-600">share & connect</span>
          </h1>
          
          <p class="mt-4 text-xl text-zinc-500 max-w-2xl mx-auto leading-relaxed">
            Express yourself freely, find people who understand, and support each other in a community built on empathy.
          </p>
          
          <div class="mt-10 flex flex-col sm:flex-row gap-4 justify-center">
            <router-link
              :to="isAuthenticated ? '/home' : '/signup'"
              class="inline-flex items-center justify-center px-8 py-4 text-base font-bold text-white bg-zinc-900 rounded-full hover:bg-violet-600 hover:shadow-xl hover:-translate-y-1 transition-all duration-300"
            >
              Start Venting
              <ArrowRight class="ml-2 h-5 w-5" />
            </router-link>
            <a
              href="#features"
              class="inline-flex items-center justify-center px-8 py-4 text-base font-bold text-zinc-700 bg-white border border-zinc-200 rounded-full hover:bg-zinc-50 hover:border-zinc-300 transition-all duration-300"
            >
              Learn more
            </a>
          </div>
          
          <!-- Social Proof / Stats placeholder -->
          <div class="mt-12 pt-8 border-t border-zinc-200/50 flex justify-center items-center gap-8 text-zinc-400 grayscale opacity-70">
             <div class="flex items-center gap-2"><Users class="h-5 w-5" /><span class="font-semibold">Community</span></div>
             <div class="flex items-center gap-2"><ShieldCheck class="h-5 w-5" /><span class="font-semibold">Safe Space</span></div>
             <div class="flex items-center gap-2"><Heart class="h-5 w-5" /><span class="font-semibold">Support</span></div>
          </div>
        </div>
      </div>
    </main>

    <!-- Features Section -->
    <section id="features" class="py-24 bg-white relative">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center max-w-3xl mx-auto mb-16">
          <h2 class="text-base font-bold text-violet-600 uppercase tracking-wide">Features</h2>
          <p class="mt-2 text-3xl font-extrabold text-zinc-900 sm:text-4xl">Everything you need to feel heard</p>
          <p class="mt-4 text-lg text-zinc-500">We've built a platform that prioritizes your mental well-being and genuine connection over metrics.</p>
        </div>

        <div class="grid md:grid-cols-3 gap-8">
          <!-- Feature 1 -->
          <div class="group p-8 rounded-3xl bg-zinc-50 border border-zinc-100 hover:border-violet-200 hover:bg-violet-50/30 transition-all duration-300">
            <div class="w-14 h-14 bg-white rounded-2xl flex items-center justify-center shadow-sm text-violet-600 mb-6 group-hover:scale-110 transition-transform duration-300">
              <MessageSquare class="h-7 w-7" />
            </div>
            <h3 class="text-xl font-bold text-zinc-900 mb-3">Express Freely</h3>
            <p class="text-zinc-500 leading-relaxed">
              Share your daily experiences, thoughts, and feelings without judgment. Use markdown to format your stories.
            </p>
          </div>

          <!-- Feature 2 -->
          <div class="group p-8 rounded-3xl bg-zinc-50 border border-zinc-100 hover:border-violet-200 hover:bg-violet-50/30 transition-all duration-300">
            <div class="w-14 h-14 bg-white rounded-2xl flex items-center justify-center shadow-sm text-violet-600 mb-6 group-hover:scale-110 transition-transform duration-300">
              <Wallet class="h-7 w-7" />
            </div>
            <h3 class="text-xl font-bold text-zinc-900 mb-3">Earn Support</h3>
            <p class="text-zinc-500 leading-relaxed">
              Receive donations from users who resonate with your story. Add your payment methods easily.
            </p>
          </div>

          <!-- Feature 3 -->
          <div class="group p-8 rounded-3xl bg-zinc-50 border border-zinc-100 hover:border-violet-200 hover:bg-violet-50/30 transition-all duration-300">
            <div class="w-14 h-14 bg-white rounded-2xl flex items-center justify-center shadow-sm text-violet-600 mb-6 group-hover:scale-110 transition-transform duration-300">
              <MessageCircle class="h-7 w-7" />
            </div>
            <h3 class="text-xl font-bold text-zinc-900 mb-3">Private Chat</h3>
            <p class="text-zinc-500 leading-relaxed">
              Connect deeper with private messaging. Send requests to chat with people who inspire you.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- How it works / Secondary Section -->
    <section id="how-it-works" class="py-24 bg-zinc-900 text-white overflow-hidden relative">
        <!-- Background accents -->
        <div class="absolute top-0 right-0 w-[600px] h-[600px] bg-violet-600/20 rounded-full blur-[100px] pointer-events-none translate-x-1/2 -translate-y-1/2"></div>
        <div class="absolute bottom-0 left-0 w-[400px] h-[400px] bg-indigo-600/20 rounded-full blur-[100px] pointer-events-none -translate-x-1/2 translate-y-1/2"></div>

        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
            <div class="grid lg:grid-cols-2 gap-16 items-center">
                <div>
                    <h2 class="text-3xl sm:text-4xl font-extrabold tracking-tight mb-6">
                        Connect with purpose
                    </h2>
                    <p class="text-zinc-400 text-lg mb-8 leading-relaxed">
                        Meaningful connections start with a simple hello. Request to connect with authors, get approved, and start a private conversation or send support.
                    </p>
                    
                    <div class="space-y-6">
                        <div class="flex items-start">
                            <div class="flex-shrink-0 w-10 h-10 rounded-full bg-zinc-800 flex items-center justify-center text-violet-400 border border-zinc-700">
                                <span class="font-bold">1</span>
                            </div>
                            <div class="ml-4">
                                <h4 class="text-lg font-bold">Discover Stories</h4>
                                <p class="text-zinc-400 mt-1">Browse the feed to find stories that resonate with you.</p>
                            </div>
                        </div>
                        <div class="flex items-start">
                            <div class="flex-shrink-0 w-10 h-10 rounded-full bg-zinc-800 flex items-center justify-center text-violet-400 border border-zinc-700">
                                <span class="font-bold">2</span>
                            </div>
                            <div class="ml-4">
                                <h4 class="text-lg font-bold">Connect & Chat</h4>
                                <p class="text-zinc-400 mt-1">Send a connection request to start a private dialogue.</p>
                            </div>
                        </div>
                        <div class="flex items-start">
                            <div class="flex-shrink-0 w-10 h-10 rounded-full bg-zinc-800 flex items-center justify-center text-violet-400 border border-zinc-700">
                                <span class="font-bold">3</span>
                            </div>
                            <div class="ml-4">
                                <h4 class="text-lg font-bold">Show Appreciation</h4>
                                <p class="text-zinc-400 mt-1">Like, comment, or send a donation to show you care.</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="relative">
                    <!-- Abstract representation of UI -->
                    <div class="bg-zinc-800/50 backdrop-blur-sm border border-zinc-700 rounded-2xl p-6 shadow-2xl transform rotate-2 hover:rotate-0 transition-transform duration-500">
                        <div class="flex items-center space-x-3 mb-4">
                            <div class="w-10 h-10 rounded-full bg-zinc-700"></div>
                            <div class="space-y-2">
                                <div class="w-32 h-4 bg-zinc-700 rounded"></div>
                                <div class="w-20 h-3 bg-zinc-700/50 rounded"></div>
                            </div>
                        </div>
                        <div class="space-y-3">
                            <div class="w-full h-3 bg-zinc-700/30 rounded"></div>
                            <div class="w-full h-3 bg-zinc-700/30 rounded"></div>
                            <div class="w-3/4 h-3 bg-zinc-700/30 rounded"></div>
                        </div>
                        <div class="mt-6 flex gap-3">
                            <div class="w-20 h-8 bg-violet-600 rounded-full opacity-80"></div>
                            <div class="w-20 h-8 bg-zinc-700 rounded-full"></div>
                        </div>
                    </div>
                     <div class="absolute -bottom-10 -left-10 bg-zinc-800/80 backdrop-blur-md border border-zinc-700 rounded-2xl p-4 shadow-xl transform -rotate-3 hover:rotate-0 transition-transform duration-500 max-w-xs">
                        <div class="flex items-center gap-3">
                            <div class="w-8 h-8 rounded-full bg-emerald-500/20 flex items-center justify-center">
                                <Heart class="w-4 h-4 text-emerald-500" />
                            </div>
                            <div>
                                <p class="text-sm font-bold">New Donation!</p>
                                <p class="text-xs text-zinc-400">Someone supported your story.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="bg-white border-t border-zinc-100 py-12">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row justify-between items-center gap-6">
            <div class="flex items-center gap-2">
                <div class="w-6 h-6 bg-zinc-900 rounded flex items-center justify-center text-white">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
                </div>
                <span class="text-lg font-bold text-zinc-900">VentingApp</span>
            </div>
            <div class="flex space-x-6 text-sm text-zinc-500">
                <a href="#" class="hover:text-zinc-900 transition-colors">Privacy</a>
                <a href="#" class="hover:text-zinc-900 transition-colors">Terms</a>
                <a href="#" class="hover:text-zinc-900 transition-colors">Support</a>
            </div>
            <p class="text-sm text-zinc-400">
                &copy; {{ new Date().getFullYear() }} VentingApp. All rights reserved.
            </p>
        </div>
    </footer>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useUserStore } from '@/stores/user';
import { MessageSquare, Users, Wallet, Check, Send, ArrowRight, ShieldCheck, Heart, MessageCircle } from 'lucide-vue-next';

const userStore = useUserStore();
const isAuthenticated = computed(() => userStore.isAuthenticated);

const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
};
</script>