<script setup lang="ts">
// 新增/编辑用户的弹窗表单（新增和编辑共用）
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { addUser, updateUser } from '../api/user'
import type { User, UserForm } from '../types/user'

// defineProps 直接写类型，比 JS 版的 { modelValue: Boolean, editing: Object } 精确得多
const props = defineProps<{
  modelValue: boolean
  editing: User | null // 正在编辑的用户；null = 新增
}>()
const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  success: []
}>()

// 表单 ref：标成 Element Plus 的 FormInstance，才能点出 validate() / clearValidate()
const formRef = ref<FormInstance>()
const form = ref<UserForm>({ name: '', email: '', phone: '', role: 'viewer', status: 1 })
const submitting = ref(false)

// 校验规则：标成 FormRules（声明式，对照 jQuery 的逐个 if 判断）
const rules: FormRules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '邮箱格式不正确', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1\d{10}$/, message: '手机号格式不正确', trigger: 'blur' }
  ]
}

// 弹窗打开时：根据是新增还是编辑，初始化表单
watch(
  () => props.modelValue,
  (visible) => {
    if (!visible) return
    if (props.editing) {
      form.value = { ...props.editing } // 编辑：填入现有数据
    } else {
      form.value = { name: '', email: '', phone: '', role: 'viewer', status: 1 } // 新增：默认值
    }
    formRef.value?.clearValidate() // 清除上一次可能残留的校验红字
  }
)

function close() {
  emit('update:modelValue', false) // 通知父组件关闭
}

async function handleSubmit() {
  try {
    await formRef.value?.validate() // 统一校验
  } catch {
    return // 校验不通过
  }
  submitting.value = true
  try {
    if (props.editing) {
      // 编辑时一定有 id，用 !（非空断言）告诉 TS「这里 id 不是 undefined」
      await updateUser(form.value.id!, form.value)
      ElMessage.success('修改成功')
    } else {
      await addUser(form.value)
      ElMessage.success('新增成功')
    }
    emit('success') // 通知父组件刷新列表
    close()
  } catch (e) {
    // catch 里的 e 是 unknown 类型（TS 不让你随便 .message），先断言成 Error
    ElMessage.error('保存失败：' + (e as Error).message)
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <el-dialog
    :model-value="modelValue"
    @update:model-value="emit('update:modelValue', $event)"
    :title="editing ? '编辑用户' : '新增用户'"
    width="480px"
  >
    <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
      <el-form-item label="姓名" prop="name">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="邮箱" prop="email">
        <el-input v-model="form.email" />
      </el-form-item>
      <el-form-item label="手机" prop="phone">
        <el-input v-model="form.phone" />
      </el-form-item>
      <el-form-item label="角色" prop="role">
        <el-select v-model="form.role" style="width: 100%">
          <el-option label="管理员" value="admin" />
          <el-option label="编辑" value="editor" />
          <el-option label="访客" value="viewer" />
        </el-select>
      </el-form-item>
      <el-form-item label="状态" prop="status">
        <el-switch
          v-model="form.status"
          :active-value="1"
          :inactive-value="0"
          active-text="启用"
          inactive-text="禁用"
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button @click="close">取消</el-button>
      <el-button type="primary" :loading="submitting" @click="handleSubmit">保存</el-button>
    </template>
  </el-dialog>
</template>
