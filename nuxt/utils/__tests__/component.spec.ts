import { mount } from '@vue/test-utils'
import { Vue, Component, Prop } from 'vue-property-decorator'
import { DataTransformer } from '../component'
import { $nextTick } from '@/utils/test/promise'

describe('DataTransformer', () => {
  describe('Sync', () => {

    const Double = DataTransformer(value => value * 2)

    @Component
    class Comp extends Vue {
      @Prop({ required: true })
      value: number

      @Double('value')
      double: number = 0
      render() { }
    }

    function getWrapper() {
      return mount(
        {
          template: '<p>value</p>',
          extends: Comp
        } as any, {
          propsData: {
            value: 1
          }
        })
    }

    test('initial state', async () => {
      const wrapper = getWrapper()
      const vm: Comp = wrapper.vm as any
      expect(vm.value).toBe(1)
      expect(vm.double).toBe(2)
    })

    test('initial state', async () => {
      const wrapper = getWrapper()
      const vm: Comp = wrapper.vm as any
      expect(vm.value).toBe(1)
      expect(vm.double).toBe(2)
      wrapper.setProps({
        value: 2
      })
      expect(vm.value).toBe(2)
      expect(vm.double).toBe(4)
    })
  })

  describe('Async', () => {
    const AsyncDouble = DataTransformer(async value => {
      await $nextTick()
      return value * 2
    })

    @Component
    class Comp extends Vue {
      @Prop({ required: true })
      value: number

      @AsyncDouble('value')
      double: number = 0
      render() { }
    }

    function getWrapper() {
      return mount(
        {
          template: '<p>value</p>',
          extends: Comp
        } as any, {
          propsData: {
            value: 1
          }
        })
    }

    test('initial state', async () => {
      const wrapper = getWrapper()
      const vm: Comp = wrapper.vm as any
      expect(vm.value).toBe(1)
      expect(vm.double).toBe(0)
      await $nextTick()
      await $nextTick()
      expect(vm.double).toBe(2)
    })

    test('initial state', async () => {
      const wrapper = getWrapper()
      const vm: Comp = wrapper.vm as any
      await $nextTick()
      await $nextTick()
      expect(vm.value).toBe(1)
      expect(vm.double).toBe(2)
      wrapper.setProps({
        value: 2
      })
      expect(vm.value).toBe(2)
      expect(vm.double).toBe(2)
      await $nextTick()
      await $nextTick()
      expect(vm.value).toBe(2)
      expect(vm.double).toBe(4)
    })
  })
})
