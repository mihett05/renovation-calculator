import { useLazySearchFloorsApiV1CatalogSearchFloorsGetQuery } from '~/shared/api/api';
import BaseSearch from '~/shared/ui/search';
import { useDebounce } from '~/shared/utils/debounce';

function SearchFloors() {
  const [querySearch, searchResult] =
    useLazySearchFloorsApiV1CatalogSearchFloorsGetQuery();

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
      label="Отделка пола"
      startSearch={startSearch}
      result={searchResult.data?.floors}
      isLoading={searchResult.isFetching}
    />
  );
}

export default SearchFloors;
