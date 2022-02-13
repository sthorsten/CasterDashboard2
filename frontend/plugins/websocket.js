export default ({ app, store, route }, inject) => {
  app.router.beforeEach(async (to, from, next) => {
    // Dashboard Websocket
    const fromDashboard = from.path.split('/').indexOf('dashboard') === 1
    const toDashboard = to.path.split('/').indexOf('dashboard') === 1

    const toMatch = to.path.split('/').indexOf('matches') === 2

    if (!fromDashboard && toDashboard) {
      await store.dispatch('coreSocket/connect')
      await store.dispatch('mainSocket/connect')
      await store.dispatch('matchSocket/connect')
    } else if (!toDashboard && store.state.coreSocket.connected) {
      store.dispatch('coreSocket/disconnect')
      store.dispatch('mainSocket/disconnect')
      store.dispatch('matchSocket/disconnect')
    }

    if (toMatch && to.params.matchID) {
      if (from.params.matchID !== to.params.matchID) {
        await store.dispatch('matchSocket/getMatchMaps', to.params.matchID)
      }
    }

    return next()
  })
}
