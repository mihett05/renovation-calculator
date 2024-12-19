import {
  Box,
  Card,
  Grid,
  Group,
  NumberInput,
  SimpleGrid,
  Stack,
  TextInput,
} from '@mantine/core';
import { useState } from 'react';
import { WallCard } from '~/entities/wall';
import {
  useGetFloorsCatalogApiV1CatalogFloorsGetQuery,
  useGetWallsCatalogApiV1CatalogWallsGetQuery,
} from '~/shared/api/api';
import Layout from '~/shared/ui/layout';
import { useDebounce } from '~/shared/utils/debounce';

type Criterias = {
  name?: string;
  color?: string;
  minPrice?: number;
  maxPrice?: number;
};

const PAGE_SIZE = 400;
const TIMEOUT = 500;

function Catalog() {
  const [objectType, setObjectType] = useState<'walls' | 'floors'>('walls');
  const [criterias, setCriterias] = useState<Criterias>({});
  const [page, setPage] = useState(0);

  const { isFetching, isError, data } =
    useGetWallsCatalogApiV1CatalogWallsGetQuery(
      {
        name: criterias.name,
        color: criterias.color,
        priceMax: criterias.maxPrice,
        priceMin: criterias.minPrice,
        page,
        pageSize: PAGE_SIZE,
      },
      {
        refetchOnMountOrArgChange: true,
      },
    );

  console.log(criterias);

  const changeName = useDebounce((name?: string) => {
    setCriterias((old) => ({
      ...old,
      name,
    }));
  }, TIMEOUT);

  const changeColor = useDebounce((color?: string) => {
    setCriterias((old) => ({
      ...old,
      color,
    }));
  }, TIMEOUT);

  const changeMinPrice = useDebounce((minPrice?: number) => {
    setCriterias((old) => ({
      ...old,
      minPrice,
    }));
  }, TIMEOUT);

  const changeMaxPrice = useDebounce((maxPrice?: number) => {
    setCriterias((old) => ({
      ...old,
      maxPrice,
    }));
  }, TIMEOUT);

  const objects = data?.walls || [];

  return (
    <Layout
      asideConfig={{
        width: 400,
        breakpoint: 'sm',
        collapsed: {
          desktop: false,
          mobile: true,
        },
      }}
      aside={
        <Stack p={15}>
          <TextInput
            label="Цвет"
            value={criterias.color}
            onChange={(e) => changeColor(e.target.value)}
          />

          <Group>
            <NumberInput
              label="Мин. цена"
              size="sm"
              min={0}
              w="10em"
              flex={1}
              value={criterias.minPrice}
              onValueChange={(v) => changeMinPrice(v.floatValue)}
              max={criterias.maxPrice}
            />
            <NumberInput
              label="Макс. цена"
              size="sm"
              w="10em"
              flex={1}
              value={criterias.maxPrice}
              onValueChange={(v) => changeMaxPrice(v.floatValue)}
            />
          </Group>
        </Stack>
      }
    >
      <Box>
        <TextInput
          label="Наименование"
          value={criterias.name}
          onChange={(e) => changeName(e.target.value)}
        />
      </Box>
      <SimpleGrid cols={5} p={15}>
        {objects.map((object) => (
          <WallCard wall={object} key={object.uid} />
        ))}
      </SimpleGrid>
    </Layout>
  );
}

export default Catalog;
