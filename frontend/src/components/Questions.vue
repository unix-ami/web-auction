<template>
  <div class="questions-section mt-5">
    <h4>Questions & Answers</h4>
    
    <!-- Ask question form (if not owner) -->
    <div v-if="!item.is_owner" class="card mb-4">
      <div class="card-body">
        <h5 class="card-title">Ask a Question</h5>
        <textarea v-model="newQuestion" class="form-control mb-2" rows="3" 
                  placeholder="Ask the seller about this item..."></textarea>
        <button @click="submitQuestion" class="btn btn-primary" :disabled="!newQuestion.trim()">  <!-- enables if text exists -->
          Submit Question
        </button>
      </div>
    </div>
    
    <!-- Questions list -->
    <div v-if="loading">Loading questions...</div>
    <div v-else-if="questions.length === 0" class="alert alert-info">
       <span v-if="!item.is_owner">No questions yet. Be the first to ask!</span>
       <span v-else>No questions have been asked yet.</span>
    </div>
    
    <div v-else class="questions-list">
      <div v-for="question in questions" :key="question.id" class="card mb-3">
        <div class="card-body">
          <!-- Question -->
          <div class="d-flex align-items-start mb-3">
            <img v-if="question.user.profile_image" 
                 :src="question.user.profile_image" 
                 :alt="question.user.username"
                 class="rounded-circle me-3"
                 style="width: 40px; height: 40px; object-fit: cover;">
            <div>
              <strong>{{ question.user.username }}</strong>
              <small class="text-muted ms-2">{{ formatDate(question.created_at) }}</small>
              <p class="mb-0 mt-1">{{ question.text }}</p>
            </div>
          </div>
          
          <!-- Answer (if exists) -->
          <div v-if="question.answer" class="answer ms-5 ps-3 border-start border-3">
            <div class="d-flex align-items-start">
              <img v-if="item.seller_profile_image" 
                   :src="item.seller_profile_image" 
                   :alt="item.seller"
                   class="rounded-circle me-3"
                   style="width: 40px; height: 40px; object-fit: cover;">
              <div>
                <strong>{{ item.seller }}</strong> (seller)
                <small class="text-muted ms-2">{{ formatDate(question.answered_at) }}</small>
                <p class="mb-0 mt-1">{{ question.answer }}</p>
              </div>
            </div>
          </div>
          
          <!-- Answer form (if owner and no answer) -->
          <div v-else-if="item.is_owner" class="answer-form ms-5 mt-3">
            <textarea v-model="answerTexts[question.id]" 
                      class="form-control mb-2" 
                      rows="2"
                      placeholder="Type your answer..."></textarea>
            <button @click="submitAnswer(question.id)" 
                    class="btn btn-sm btn-success"
                    :disabled="!answerTexts[question.id]?.trim()">
              Post Answer
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";

interface User {
  id: number;
  username: string;
  profile_image: string | null;
}

interface Question {
  id: number;
  text: string;
  answer: string | null;
  created_at: string;
  answered_at: string | null;
  user: User;
}

interface Item {
  id: number;
  is_owner: boolean;
  seller: string;
  seller_profile_image?: string;
}

export default defineComponent({
  name: "Questions",
  props: {
    item: {
      type: Object as PropType<Item>,  // Tells TS this prop is an Item object
      required: true,
    },
  },
  data() {
    return {
      questions: [] as Question[],
      newQuestion: "",
      answerTexts: {} as Record<number, string>, // Object with id/key, string value
      loading: false,
      error: "",
    };
  },
  methods: {
    getCSRFToken(): string {
      const name = "csrftoken";
      let cookieValue = "";
      if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === name + "=") {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    },
    
    async fetchQuestions() {
      this.loading = true;
      try {
        const response = await fetch(`/api/item/${this.item.id}/questions/`, {
          credentials: "include",
        });
        this.questions = await response.json();
      } catch (err) {
        console.error("Failed to fetch questions:", err);
      } finally {
        this.loading = false;
      }
    },
    
    async submitQuestion() {
      if (!this.newQuestion.trim()) return;
      
      try {
        const csrfToken = this.getCSRFToken();
        const response = await fetch(`/api/item/${this.item.id}/ask/`, {
          method: "POST",
          headers: { 
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
          },
          credentials: "include",
          body: JSON.stringify({ text: this.newQuestion }), //convert JS obj to JSON string
        });
        
        if (response.ok) {
          this.newQuestion = "";  // Clear the question input field
          this.fetchQuestions();  // Refresh the questions list
        } else {
          console.error("Failed to submit question:", await response.json());
        }
      } catch (err) {
        console.error("Failed to submit question:", err);
      }
    },
    
    async submitAnswer(questionId: number) {
      const answer = this.answerTexts[questionId];
      if (!answer?.trim()) return; // Prevents empty answers
      
      try {
        const csrfToken = this.getCSRFToken();
        const response = await fetch(`/api/question/${questionId}/answer/`, {
          method: "POST",
          headers: { 
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
          },
          credentials: "include",
          body: JSON.stringify({ answer: answer }),
        });
        
        if (response.ok) {
          this.answerTexts[questionId] = ""; // Clear the ans input field for q
          this.fetchQuestions();             // Refresh the q list to show the new ans
        }
      } catch (err) {
        console.error("Failed to submit answer:", err);
      }
    },
    
    formatDate(dateString: string | null): string {
      if (!dateString) return "";
      const date = new Date(dateString);
      return date.toLocaleDateString() + " " + 
             date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    },
  },
  mounted() {
    this.fetchQuestions();
  },
});
</script>