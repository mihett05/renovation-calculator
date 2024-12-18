import { Box, Group, Image, Loader, Select, Text } from '@mantine/core';
import { useState } from 'react';

type GenericObject = {
  name: string;
  photo: string;
};

type BaseSearchProps = {
  startSearch: (value: string) => void;
  result?: GenericObject[];
  isLoading: boolean;
  label: string;
};

function BaseSearch({
  label,
  startSearch,
  result,
  isLoading,
}: BaseSearchProps) {
  const [search, setSearch] = useState('');

  return (
    <Select
      label={label}
      searchable
      nothingFoundMessage={
        isLoading
          ? 'Загрузка...'
          : search.trim().length > 0
            ? 'Ничего не найдено'
            : 'Начните вводить для поиска...'
      }
      searchValue={search}
      onSearchChange={(value) => {
        setSearch(value);
        startSearch(value);
      }}
      data={
        result?.map((object) => ({
          value: JSON.stringify(object),
          label: object.name,
        })) || []
      }
      renderOption={(item) => {
        const object = JSON.parse(item.option.value) as GenericObject;
        return (
          <Group>
            <Box>
              <Image src={object.photo} radius="md" height={64} width={64} />
            </Box>
            <Text flex={1}>{item.option.label}</Text>
          </Group>
        );
      }}
      rightSection={isLoading && <Loader size={24} />}
    />
  );
}

export default BaseSearch;
