<template>
  <div class="col">
    <!-- Different border colors for owned vs not owned -->
    <div class="card h-100 shadow-sm" :class="item.is_owner ? 'border-secondary' : 'border-primary'">
      <img 
        :src="item.image || '/placeholder.jpg'" 
        :alt="item.title" 
        class="card-img-top"
        style="height: 180px; object-fit: cover;"
      >
      <div class="card-body d-flex flex-column">
        <h6 class="card-title mb-3">{{ item.title }}</h6>
        
        <div class="mt-auto">
          <!-- price and time on the left -->
          <div class="d-flex justify-content-between align-items-center mb-3">
            <div>
              <small class="text-muted d-block">Starting price</small>
              <span class="h5" :class="item.is_owner ? 'text-secondary' : 'text-primary'">
                £{{ item.starting_price }}
              </span>
            </div>
            
            <!-- time on the right - different colors -->
            <div>
              <small class="badge" :class="item.is_owner ? 'bg-secondary text-white' : 'bg-primary text-white'">
                {{ timeLeftBadge(item.auction_end) }}
              </small>
            </div>
          </div>
          
          <!-- Different button text and colors -->
          <router-link 
            :to="{ name: 'Item Detail Page', params: { id: item.id } }" 
            class="btn w-100 btn-sm"
            :class="item.is_owner ? 'btn-outline-secondary' : 'btn-outline-primary'"
          >
            {{ item.is_owner ? 'View questions on your item' : 'View details to bid' }}
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";

interface Item {
  id: number;
  title: string;
  description: string;
  starting_price: string;
  image: string | null;
  auction_end: string;
  is_owner: boolean; 
}

export default defineComponent({
  name: "Item",
  props: {
    item: {
      type: Object as PropType<Item>,
      required: true,
    },
  },
  methods: {
    timeLeftBadge(endDate: string): string {
      const end = new Date(endDate);
      const now = new Date();
      const diff = end.getTime() - now.getTime();
      
      if (diff <= 0) return 'Ended';
      
      const days = Math.floor(diff / (1000 * 60 * 60 * 24));
      const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      
      if (days > 0) return `${days}d left`;
      return `${hours}h left`;
    }
  }
});
</script>