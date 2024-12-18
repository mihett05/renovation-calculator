import { useLazySearchWallsApiV1CatalogSearchWallsGetQuery } from '~/shared/api/api';
import BaseSearch from '~/shared/ui/search';
import { useDebounce } from '~/shared/utils/debounce';

function SearchWalls() {
  const [querySearch, searchResult] =
    useLazySearchWallsApiV1CatalogSearchWallsGetQuery();

  const startSearch = useDebounce((value: string) => {
    if (value.trim().length > 0) {
      querySearch({
        search: value,
        limit: 10,
      });
    }
  }, 500);

  return (
    <BaseSearch
      label="Отделка стен"
      startSearch={startSearch}
      result={searchResult.data?.walls}
      isLoading={searchResult.isFetching}
    />
  );
}

export default SearchWalls;
