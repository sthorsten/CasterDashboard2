export interface Match {
  id: number;
  creatorName?: string;
  leagueName: string;
  playdayName?: string;
  tournamentName?: string;
  teamBlueName: string;
  teamOrangeName: string;
  winTeamName?: string;
  date: string | Date;
  created: string | Date;
  lastModified: string | Date;
  name: string;
  title: string;
  subTitle: string;
  shareMode: string;
  bestOf: number;
  status: MatchStatus,
  scoreBlue: number;
  scoreOrange: number;
  winType: string;
  creator: null;
  league: number;
  playday?: number;
  tournament?: number;
  teamBlue: number;
  teamOrange: number;
  winTeam?: number;
  additionalUsers: number[];
}

export enum MatchStatus {
  "CREATED" = "CREATED",
  "MAP_BAN" = "MAP_BAN",
  "PLAYING" = "PLAYING",
  "CLOSED" = "CLOSED",
  "ARCHIVED" = "ARCHIVED",
  "DUMMY" = "DUMMY"
}
