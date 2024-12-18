import { baseApi as api } from "./baseApi";
const injectedRtkApi = api.injectEndpoints({
  endpoints: (build) => ({
    getWallsCatalogApiV1CatalogWallsGet: build.query<
      GetWallsCatalogApiV1CatalogWallsGetApiResponse,
      GetWallsCatalogApiV1CatalogWallsGetApiArg
    >({
      query: () => ({ url: `/api/v1/catalog/walls` }),
    }),
    getFloorsCatalogApiV1CatalogFloorsGet: build.query<
      GetFloorsCatalogApiV1CatalogFloorsGetApiResponse,
      GetFloorsCatalogApiV1CatalogFloorsGetApiArg
    >({
      query: () => ({ url: `/api/v1/catalog/floors` }),
    }),
    searchWallsApiV1CatalogSearchWallsGet: build.query<
      SearchWallsApiV1CatalogSearchWallsGetApiResponse,
      SearchWallsApiV1CatalogSearchWallsGetApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/catalog/search/walls`,
        params: {
          search: queryArg.search,
          limit: queryArg.limit,
        },
      }),
    }),
    searchFloorsApiV1CatalogSearchFloorsGet: build.query<
      SearchFloorsApiV1CatalogSearchFloorsGetApiResponse,
      SearchFloorsApiV1CatalogSearchFloorsGetApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/catalog/search/floors`,
        params: {
          search: queryArg.search,
          limit: queryArg.limit,
        },
      }),
    }),
  }),
  overrideExisting: false,
});
export { injectedRtkApi as api };
export type GetWallsCatalogApiV1CatalogWallsGetApiResponse =
  /** status 200 Successful Response */ any;
export type GetWallsCatalogApiV1CatalogWallsGetApiArg = void;
export type GetFloorsCatalogApiV1CatalogFloorsGetApiResponse =
  /** status 200 Successful Response */ any;
export type GetFloorsCatalogApiV1CatalogFloorsGetApiArg = void;
export type SearchWallsApiV1CatalogSearchWallsGetApiResponse =
  /** status 200 Successful Response */ WallsSearch;
export type SearchWallsApiV1CatalogSearchWallsGetApiArg = {
  search: string;
  limit: number;
};
export type SearchFloorsApiV1CatalogSearchFloorsGetApiResponse =
  /** status 200 Successful Response */ FloorsSearch;
export type SearchFloorsApiV1CatalogSearchFloorsGetApiArg = {
  search: string;
  limit: number;
};
export type WallType = "wallpaper" | "paint" | "ceramic";
export type Wall = {
  uid: string;
  name: string;
  url: string;
  price: number;
  wallType: WallType;
  color: string;
  photo: string;
};
export type WallsSearch = {
  walls: Wall[];
};
export type ValidationError = {
  loc: (string | number)[];
  msg: string;
  type: string;
};
export type HttpValidationError = {
  detail?: ValidationError[];
};
export type FloorType = "linoleum" | "laminate" | "paint" | "ceramic";
export type Floor = {
  uid: string;
  name: string;
  url: string;
  price: number;
  floorType: FloorType;
  color: string;
  photo: string;
};
export type FloorsSearch = {
  floors: Floor[];
};
export const {
  useGetWallsCatalogApiV1CatalogWallsGetQuery,
  useLazyGetWallsCatalogApiV1CatalogWallsGetQuery,
  useGetFloorsCatalogApiV1CatalogFloorsGetQuery,
  useLazyGetFloorsCatalogApiV1CatalogFloorsGetQuery,
  useSearchWallsApiV1CatalogSearchWallsGetQuery,
  useLazySearchWallsApiV1CatalogSearchWallsGetQuery,
  useSearchFloorsApiV1CatalogSearchFloorsGetQuery,
  useLazySearchFloorsApiV1CatalogSearchFloorsGetQuery,
} = injectedRtkApi;
