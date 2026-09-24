import { defineStore } from 'pinia'

interface Item {
  id: number
  title: string
  description: string
  starting_price: string
  image: string | null
  auction_end: string
  is_owner: boolean
}

export const useItemsStore = defineStore('items', {
  state: () => ({
    items: [] as Item[],
    searchQuery: '' as string,
    loading: false,
    error: '' as string,
  }),
  
  getters: {
    filteredItems: (state) => {
      if (!state.searchQuery.trim()) {
        return state.items
      }
      
      const query = state.searchQuery.toLowerCase().trim()
      return state.items.filter(item => {
        return (
          item.title.toLowerCase().includes(query) ||
          item.description.toLowerCase().includes(query)
        )
      })
    }
  },
  
  actions: {
    setSearchQuery(query: string): void {
      this.searchQuery = query
    },
    
    async fetchItems(): Promise<void> {
      this.loading = true
      this.error = ''
      
      try {
        const response = await fetch("/api/items/", {
          credentials: "include",
        })
        
        if (response.status === 401) {
          this.error = "Please login to view items"
          return
        }
        
        if (!response.ok) {
          throw new Error(`Failed to load items (${response.status})`)
        }
        
        const itemsData = await response.json()
        
        // Filter out ended auctions
        this.items = itemsData.filter((item: Item) => 
          new Date(item.auction_end) > new Date()
        )
        
      } catch (err: any) {
        this.error = err.message || "Failed to load items"
      } finally {
        this.loading = false
      }
    }
  },
})