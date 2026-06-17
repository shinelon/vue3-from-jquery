<template>
  <button class="my-btn"><slot>点我</slot></button>
</template>

<style scoped>
.my-btn {
  background: #42b883;
  color: #fff;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}
</style>
