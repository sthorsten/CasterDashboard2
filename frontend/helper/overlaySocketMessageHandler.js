export default function handleMessage(event, commit) {
  const data = JSON.parse(event.data)

  if (data.model === 'CustomDesignStyle') {
    if (data.partition === 'full') {
      commit('setCustomDesignStyles', data.data)
    } else if (data.partition === 'single') {
      commit('updateCustomDesignStyles', data.data)
    }
  } else if (data.model === 'UserOverlay') {
    if (data.partition === 'single') {
      commit('setUserOverlay', data.data)
    }
  }
}
