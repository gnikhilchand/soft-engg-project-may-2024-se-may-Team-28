// src/types/jwt-decode.d.ts
declare module 'jwt-decode' {
    function jwtDecode<T = any>(token: string): T;
    export = jwtDecode;
  }
  