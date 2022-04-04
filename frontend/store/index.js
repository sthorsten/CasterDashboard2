export const state = () => ({
  version: '0.0.0'
})

export const mutations = {
  setVersion(state, version) {
    state.version = version
  }
}
