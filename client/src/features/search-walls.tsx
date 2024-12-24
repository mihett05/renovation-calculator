import {
  type Wall,
  useLazySearchWallsApiV1CatalogSearchWallsGetQuery,
} from '~/shared/api/api';
import BaseSearch from '~/shared/ui/search';
import { useDebounce } from '~/shared/utils/debounce';

type SearchWallsProps = {
  selected: Wall | null;
  onSelected: (wall: Wall | null) => void;
};

function SearchWalls({ selected, onSelected }: SearchWallsProps) {
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
      selected={selected}
      onSelected={(wall) => onSelected(wall as Wall)}
    />
  );
}

export default SearchWalls;
