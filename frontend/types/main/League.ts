export interface League {
  id: number;
  created: string | Date;
  lastModified: string | Date;
  name: string;
  public: boolean;
  customDesign: boolean;
  logo?: string;
  logoSmall?: string;
}