import { Box, Flex, NumberInput, Select, Stack } from '@mantine/core';
import { useState } from 'react';
import SearchFloors from '~/features/search-floors';
import SearchWalls from '~/features/search-walls';

function Calculator() {
  const [wallHeight, setWallHeight] = useState<number | null>(2);

  const [floorWidth, setFloorWidth] = useState<number | null>(10);
  const [floorHeight, setFloorHeight] = useState<number | null>(10);

  const MAX_WIDTH = 200;
  const MAX_HEIGHT = 400;

  return (
    <Flex gap={10}>
      <Box>
        <Flex
          gap={10}
          styles={{
            root: {
              alignItems: 'center',
            },
          }}
        >
          <Stack gap={10}>
            <NumberInput
              label="Ширина пола"
              value={floorWidth ?? undefined}
              onValueChange={(e) => setFloorWidth(e.floatValue || null)}
            />
            <Box
              style={{
                width: (floorWidth || 10) * 20,
                height: (floorHeight || 10) * 20,
                border: '1px solid black',
              }}
            />
          </Stack>
          <NumberInput
            label="Длина пола"
            value={floorHeight ?? undefined}
            onValueChange={(e) => setFloorHeight(e.floatValue || null)}
          />
        </Flex>
      </Box>
      <Stack>
        <Flex gap={10}>
          <NumberInput label="Высота комнаты" />
        </Flex>
        <SearchWalls />
        <SearchFloors />
      </Stack>
    </Flex>
  );
}

export default Calculator;
