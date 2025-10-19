export interface User {
  id: number;
  firstname: string;
  lastname: string;
  email: string;
  password: string;
  status: string;
  passPolicy: boolean;
  role: string;
  passExpiresAt: Date;
}
