export default ({ app, store, route }, inject) => {
  app.router.beforeEach((to, from, next) => {
    // Dashboard Websocket
    const fromDashboard = from.path.split('/').indexOf('dashboard') === 1
    const toDashboard = to.path.split('/').indexOf('dashboard') === 1

    if (!fromDashboard && toDashboard) {
      store.dispatch('coreSocket/connect')
    } else if (!toDashboard && store.state.coreSocket.connected) {
      store.dispatch('coreSocket/disconnect')
    }

    return next()
  })

  inject('coreSocket', {
    connect () {
      store.dispatch('coreSocket/connect')
    },
    disconnect () {
      store.dispatch('coreSocket/disconnect')
    },
    isConnected () {
      return store.state.coreSocket?.connected
    }
  })
}
