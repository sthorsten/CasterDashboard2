import handleMessage from '../helper/overlaySocketMessageHandler'

export const state = () => ({
  socket: null,
  connected: false,
  customDesignStyles: null,
  userOverlay: null,
})

export const mutations = {
  setSocket(state, socket) {
    state.socket = socket
  },
  setConnected(state, connected) {
    state.connected = connected
  },

  setUserOverlay(state, userOverlay) {
    state.userOverlay = userOverlay
  },

  setCustomDesignStyles(state, customDesignStyles) {
    state.customDesignStyles = customDesignStyles
  },
  updateCustomDesignStyles(state, customDesignStyle) {
    const listElem = state.customDesignStyles.findIndex(n => n.id === customDesignStyle.id)
    state.customDesignStyles[listElem] = customDesignStyle
  },
}

export const getters = {
  isConnected: (state) => {
    if (!state.socket) { return false }
    return state.socket.readyState === 1
  },
  getCustomDesignStyleByLeague: state => (leagueID) => {
    return state.customDesignStyles.find(m => m.league === leagueID)
  },
}

export const actions = {
  connect({ commit, dispatch, state }) {
    return new Promise((resolve, reject) => {
      const socket = new WebSocket(`${this.app.$config.wsBaseURL}/ws/overlays/`)
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

  disconnect({ state }) {
    state.socket.close()
  },

  getInitialData({ state }) {
    const customDesignStyles = {
      method: 'get',
      model: 'CustomDesignStyle'
    }

    state.socket.send(JSON.stringify(customDesignStyles))
  },

  getUserOverlayData({ state }, userID) {
    const userOverlayData = {
      method: "get",
      model: "UserOverlay",
      query: {
        user: userID
      }
    }
    state.socket.send(JSON.stringify(userOverlayData))
  }
}
