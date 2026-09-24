<template>
  <div class="row row-cols-1 row-cols-md-4 g-4">
    <Item 
      v-for="item in items" 
      :key="item.id" 
      :item="item" 
    />
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue'
import Item from './Item.vue'

interface ItemType {
  id: number;
  title: string;
  description: string;
  starting_price: string;
  image: string | null;
  auction_end: string;
  is_owner: boolean;
}

export default defineComponent({
  name: "ItemTable",
  components: {
    Item,
  },
  props: {
    items: {
      type: Array as PropType<ItemType[]>,
      required: true,
    },
  },
});
</script>
