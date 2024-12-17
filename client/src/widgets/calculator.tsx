import { Box, Flex, NumberInput, Select, Stack } from '@mantine/core';

function Calculator() {
  return (
    <Flex>
      <Box></Box>
      <Stack>
        <Flex gap={10}>
          <NumberInput label="Ширина комнаты" />
          <NumberInput label="Высота комнаты" />
        </Flex>
        <Select
          label="Отделка стен"
          searchable
          nothingFoundMessage="Ничего не найдено"
        />
        <Flex gap={10}>
          <NumberInput label="Ширина пола" />
          <NumberInput label="Длина пола" />
        </Flex>
        <Select
          label="Отделка пола"
          searchable
          nothingFoundMessage="Ничего не найдено"
        />
      </Stack>
    </Flex>
  );
}

export default Calculator;
