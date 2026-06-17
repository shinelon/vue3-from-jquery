<script setup>
// 第 7 章：改用 CSS Modules（NoteItem.module.css），演示类名隔离
import styles from './NoteItem.module.css'

defineProps({
  note: { type: Object, required: true }
})
</script>

<template>
  <li :class="styles.item">
    <input type="checkbox" v-model="note.done" />
    <span :class="{ [styles.done]: note.done }">{{ note.title }}</span>
  </li>
</template>
