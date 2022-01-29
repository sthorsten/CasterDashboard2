export default function handleMessage (event, commit) {
  const data = JSON.parse(event.data)

  if (data.model === 'Notification') {
    if (data.partition === 'full') {
      commit('setNotifications', data.data)
    } else if (data.partition === 'single') {
      commit('updateNotification', data.data)
    }
  } else if (data.model === 'MapPool') {
    if (data.partition === 'full') {
      commit('setMapPools', data.data)
    } else if (data.partition === 'single') {
      commit('updateMapPool', data.data)
    }
  } else if (data.model === 'Map') {
    if (data.partition === 'full') {
      commit('setMaps', data.data)
    } else if (data.partition === 'single') {
      commit('updateMap', data.data)
    }
  } else if (data.model === 'BombSpot') {
    if (data.partition === 'full') {
      commit('setBombSpots', data.data)
    } else if (data.partition === 'single') {
      commit('updateBombSpot', data.data)
    }
  } else if (data.model === 'Operator') {
    if (data.partition === 'full') {
      commit('setOperators', data.data)
    } else if (data.partition === 'single') {
      commit('updateOperator', data.data)
    }
  }
}
