import { SidebarItem } from "~~/types/SidebarItem";

export const mainSidebarItems: SidebarItem[] = [
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
    name: "Match History",
    icon: "fa-solid fa-clock-rotate-left",
    url: "/dashboard/matches/history",
  },
  {
    name: "Create a new match",
    icon: "fa-solid fa-plus",
    url: "/dashboard/matches/create",
  }
]