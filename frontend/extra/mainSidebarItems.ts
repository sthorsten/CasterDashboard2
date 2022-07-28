import { SidebarItem } from "~~/types/SidebarItem";

export const mainSidebarItems: SidebarItem[] = [
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
  }
]