import {
  type Floor,
  useLazySearchFloorsApiV1CatalogSearchFloorsGetQuery,
} from '~/shared/api/api';
import BaseSearch from '~/shared/ui/search';
import { useDebounce } from '~/shared/utils/debounce';

type SearchFloorsProps = {
  selected: Floor | null;
  onSelected: (floor: Floor | null) => void;
};

function SearchFloors({ selected, onSelected }: SearchFloorsProps) {
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
      selected={selected}
      onSelected={(floor) => onSelected(floor as Floor)}
    />
  );
}

export default SearchFloors;
