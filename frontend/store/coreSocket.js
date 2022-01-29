import handleMessage from '../helper/coreSocketMessageHandler'

export const state = () => ({
  socket: null,
  connected: false,
  notifications: [],
  mapPools: [],
  maps: [],
  bombSpots: [],
  operators: []
})

export const mutations = {
  setSocket (state, socket) {
    state.socket = socket
  },
  setConnected (state, connected) {
    state.connected = connected
  },

  setNotifications (state, notifications) {
    state.notifications = notifications
  },
  setMapPools (state, mapPools) {
    state.mapPools = mapPools
  },
  setMaps (state, maps) {
    state.maps = maps
  },
  setBombSpots (state, bombSpots) {
    state.bombSpots = bombSpots
  },
  setOperators (state, operators) {
    state.operators = operators
  },

  updateNotification (state, notification) {
    const listElem = state.notifications.findIndex(n => n.id === notification.id)
    state.notifications[listElem] = notification
  },
  updateMapPool (state, mapPool) {
    const listElem = state.mapPools.findIndex(m => m.id === mapPool.id)
    state.mapPools[listElem] = mapPool
  },
  updateMap (state, map) {
    const listElem = state.maps.findIndex(m => m.id === map.id)
    state.maps[listElem] = map
  },
  updateBombSpot (state, bombSpot) {
    const listElem = state.bombSpots.findIndex(b => b.id === bombSpot.id)
    state.bombSpots[listElem] = bombSpot
  },
  updateOperator (state, operator) {
    const listElem = state.operators.findIndex(o => o.id === operator.id)
    state.operators[listElem] = operator
  }
}

export const getters = {
  isConnected: (state) => {
    if (!state.socket) { return false }
    return state.socket.readyState === 1
  },
  getMapPool: state => (name) => {
    return state.maps.filter(m => m.name === name)[0]
  },
  getMap: state => (id) => {
    return state.maps.filter(m => m.id === id)[0]
  },
  getBombSpotsByMap: state => (mapId) => {
    return state.bombSpots.filter(b => b.map === mapId)
  },
  getOperatorsBySide: state => (side) => {
    return state.operators.filter(o => o.side === side)
  }
}

export const actions = {
  connect ({ commit, dispatch, state }) {
    return new Promise((resolve, reject) => {
      const socket = new WebSocket(`${this.app.$config.wsBaseURL}/ws/core/`)
      socket.onopen = () => {
        commit('setConnected', true)
        dispatch('getInitialData')
        resolve(socket)
      }
      socket.onmessage = (event) => {
        handleMessage(event, commit, state)
      }
      socket.onerror = error => reject(error)
      commit('setSocket', socket)
    })
  },

  disconnect ({ state }) {
    state.socket.close()
  },

  getInitialData ({ state }) {
    const notifications = {
      method: 'get',
      model: 'Notification'
    }
    const mapPools = {
      method: 'get',
      model: 'MapPool'
    }
    const maps = {
      method: 'get',
      model: 'Map'
    }
    const bombSpots = {
      method: 'get',
      model: 'BombSpot'
    }
    const operators = {
      method: 'get',
      model: 'Operator'
    }

    state.socket.send(JSON.stringify(notifications))
    state.socket.send(JSON.stringify(mapPools))
    state.socket.send(JSON.stringify(maps))
    state.socket.send(JSON.stringify(bombSpots))
    state.socket.send(JSON.stringify(operators))
  }
}
