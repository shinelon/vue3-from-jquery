<script setup>
import { ref, onMounted } from 'vue'
import NoteItem from '@/components/NoteItem.vue'
import { getNotes } from '@/api/note'

const notes = ref([])
onMounted(async () => {
  notes.value = await getNotes()
})
</script>

<template>
  <h2>笔记列表</h2>
  <ul>
    <NoteItem v-for="n in notes" :key="n.id" :note="n" />
  </ul>
</template>
