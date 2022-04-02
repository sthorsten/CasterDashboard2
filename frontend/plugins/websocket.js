export default ({ app, store, route }, inject) => {
  app.router.beforeEach(async (to, from, next) => {
    // Dashboard Websocket
    const fromDashboard = from.path.split('/').indexOf('dashboard') === 1
    const toDashboard = to.path.split('/').indexOf('dashboard') === 1

    if (!fromDashboard && toDashboard) {
      await store.dispatch('coreSocket/connect')
      await store.dispatch('mainSocket/connect')
      await store.dispatch('matchSocket/connect')
    } else if (!toDashboard && store.state.coreSocket.connected) {
      store.dispatch('coreSocket/disconnect')
      store.dispatch('mainSocket/disconnect')
      store.dispatch('matchSocket/disconnect')
    }

    // Match Websocket
    const toMatch = to.path.split('/').indexOf('matches') === 2

    if (toMatch && to.params.matchID) {
      if (from.params.matchID !== to.params.matchID) {
        await store.dispatch('matchSocket/getMatchMaps', to.params.matchID)
      }
    }

    // Overlay Websocket
    const fromOverlays = from.path.split('/').indexOf('overlays') === 2
    const toOverlays = to.path.split('/').indexOf('overlays') === 2

    if (!fromOverlays && toOverlays) {
      await store.dispatch('overlaySocket/connect')
      if (to.query.user) {
        store.dispatch('overlaySocket/getUserOverlayData', to.query.user)
      }

    } else if (!toOverlays && store.state.overlaySocket.connected) {
      store.dispatch('overlaySocket/disconnect')
    }

    return next()
  })
}
