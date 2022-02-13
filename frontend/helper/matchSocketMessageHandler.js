export default function handleMessage (event, commit) {
  const data = JSON.parse(event.data)

  if (data.model === 'Match') {
    if (data.partition === 'full') {
      commit('setMatches', data.data)
    } else if (data.partition === 'single') {
      commit('updateMatch', data.data)
    }
  } else if (data.model === 'MapBan') {
    if (data.partition === 'full') {
      commit('setMapBans', data.data)
    } else if (data.partition === 'partial') {
      data.data.forEach(m => commit('updateMapBan', m))
    } else if (data.partition === 'single') {
      commit('updateMapBan', data.data)
    }
  } else if (data.model === 'MatchMap') {
    if (data.partition === 'full') {
      commit('setMatchMaps', data.data)
    } else if (data.partition === 'partial') {
      data.data.forEach(m => commit('updateMatchMap', m))
    } else if (data.partition === 'single') {
      commit('updateMatchMap', data.data)
    }
  } else if (data.model === 'OperatorBan') {
    if (data.partition === 'full') {
      commit('setOperatorBans', data.data)
    } else if (data.partition === 'partial') {
      data.data.forEach(o => commit('updateOperatorBan', o))
    } else if (data.partition === 'single') {
      commit('updateOperatorBan', data.data)
    }
  } else if (data.model === 'Round') {
    if (data.partition === 'full') {
      commit('setRounds', data.data)
    } else if (data.partition === 'partial') {
      data.data.forEach(r => commit('updateRound', r))
    } else if (data.partition === 'single') {
      commit('updateRound', data.data)
    }
  }
}
