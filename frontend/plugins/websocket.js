export default ({ app, store, route }, inject) => {
  app.router.beforeEach(async (to, from, next) => {
    // Dashboard Websocket
    const fromDashboard = from.path.split('/').indexOf('dashboard') === 1
    const toDashboard = to.path.split('/').indexOf('dashboard') === 1

    const fromMatch = from.path.split('/').indexOf('matches') === 2
    const toMatch = to.path.split('/').indexOf('matches') === 2

    if (!fromDashboard && toDashboard) {
      await store.dispatch('coreSocket/connect')
      store.dispatch('mainSocket/connect')
    } else if (!toDashboard && store.state.coreSocket.connected) {
      store.dispatch('coreSocket/disconnect')
      store.dispatch('mainSocket/disconnect')
    }

    if (!fromMatch && toMatch) {
      if (to.params.matchID) {
        store.dispatch('matchSocket/connect', to.params.matchID)
      } else {
        store.dispatch('matchSocket/connect')
      }
    } else if (!toMatch && store.state.matchSocket.connected) {
      store.dispatch('matchSocket/disconnect')
    } else if (fromMatch && toMatch) {
      if (to.params.matchID) {
        store.dispatch('matchSocket/getMatchMaps', to.params.matchID)
      }
    }

    return next()
  })
}
