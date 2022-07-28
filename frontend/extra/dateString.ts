export const formatLocaleDate = (date: string) => {
  const dateObj = new Date(date)
  const lang = window.navigator.language
  return dateObj.toLocaleDateString(lang, { year: "numeric", month: "2-digit", day: "2-digit" })
}

export const formatLocalTime = (date: string | Date) => {
  const dateObj = new Date(date)
  const lang = window.navigator.language
  const day = dateObj.toLocaleDateString(lang, { year: "numeric", month: "2-digit", day: "2-digit" })
  const time = dateObj.toLocaleTimeString(lang, { hour: "2-digit", minute: "2-digit" })
  return `${day} - ${time}`
}