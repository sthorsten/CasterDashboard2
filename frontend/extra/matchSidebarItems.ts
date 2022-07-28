import { SidebarItem } from "~~/types/SidebarItem";

export const matchSidebarItems = (matchId?: string, mapName?: string) => {
  const baseItems = [
    {
      name: "Home",
      isHeader: true,
    },
    {
      name: "Home",
      icon: "fa-solid fa-house-chimney",
      url: "/dashboard/home",
    },
    {
      name: "Matches",
      isHeader: true,
    },
    {
      name: "Match List",
      icon: "fa-solid fa-list-ol",
      url: "/dashboard/matches/list",
    },
    {
      name: "Create a new match",
      icon: "fa-solid fa-plus",
      url: "/dashboard/matches/create",
    },
  ]

  const matchItems = matchId ? [
    {
      name: "Current Match",
      isHeader: true,
    },
    {
      name: "Match Overview",
      icon: "fa-solid fa-compass",
      url: `/dashboard/matches/${matchId}/overview`,
    },
  ] : []


  const mapItems = []

  return Array.prototype.concat(baseItems, matchItems, mapItems)
}