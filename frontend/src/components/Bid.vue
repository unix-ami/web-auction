<template>
  <div v-if="canBid" class="card mt-4">
    <div class="card-body">
      <h5 class="card-title">Place a Bid</h5>
      
      <!-- Current highest bid -->
      <div v-if="highestBid" class="alert alert-info">
        Current highest bid: <strong>£{{ highestBid.amount }}</strong>
        <small class="d-block text-muted">by {{ highestBid.user }}</small>
      </div>
      
      <!-- Bid form -->
      <div class="mb-3">
        <label for="bidAmount" class="form-label">Your Bid (£)</label>
        <input 
          v-model="bidAmount" 
          type="number" 
          id="bidAmount"
          :min="minBid" 
          step="0.01" 
          class="form-control"
          placeholder="Enter your bid amount"
        >
        <div class="form-text">Minimum bid: £{{ minBid.toFixed(2) }}</div>
      </div>
      
      <button 
        @click="placeBid" 
        class="btn btn-primary"
        :disabled="!bidAmount || bidAmount < minBid || loading"
      >
        <span v-if="loading" class="spinner-border spinner-border-sm me-1"></span>
        Place Bid
      </button>
      
      <!-- Error message -->
      <div v-if="error" class="alert alert-danger mt-3">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";

interface Bid {
  id: number;
  amount: string;
  user: string;
  created_at: string;
}

interface Item {
  id: number;
  starting_price: string;
  auction_end: string;
  is_owner: boolean;
}

export default defineComponent({
  name: "Bid",
  props: {
    item: {
      type: Object as PropType<Item>,
      required: true,
    },
  },
  data() {
    return {
      bidAmount: 0 as number,
      highestBid: null as Bid | null,
      error: "" as string,
      loading: false as boolean,
    };
  },
  computed: {
    isActive(): boolean {
      return new Date(this.item.auction_end) > new Date();
    },
    canBid(): boolean {
      return this.isActive && !this.item.is_owner;
    },
    minBid(): number {
      if (this.highestBid) {
        return parseFloat(this.highestBid.amount) + 0.01;
      }
      return parseFloat(this.item.starting_price);
    }
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
    
    async fetchBids() {
      try {
        const response = await fetch(`/api/item/${this.item.id}/bids/`, {
          credentials: 'include'
        });
        
        if (response.ok) {
          const bids = await response.json();
          this.highestBid = bids[0] || null;
        }
      } catch (err) {
        console.error('Failed to fetch bids:', err);
      }
    },
    
    async placeBid() {
      this.error = "";
      this.loading = true;
      
      if (this.bidAmount < this.minBid) {
        this.error = `Bid must be at least £${this.minBid.toFixed(2)}`;
        this.loading = false;
        return;
      }
      
      try {
        const csrfToken = this.getCSRFToken();
        const response = await fetch(`/api/item/${this.item.id}/bid/`, {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
          },
          credentials: 'include',
          body: JSON.stringify({ amount: this.bidAmount })
        });
        
        const data = await response.json();
        
        if (response.ok) {
          alert('Bid placed successfully!');
          this.bidAmount = 0;
          this.fetchBids(); // Refresh bids
          this.$emit('bid-placed'); // Notify parent
        } else {
          this.error = data.error || 'Failed to place bid';
        }
      } catch (err) {
        this.error = 'Network error. Please try again.';
      } finally {
        this.loading = false;
      }
    }
  },
  mounted() {
    this.fetchBids();
  },
  emits: ['bid-placed']
});
</script>