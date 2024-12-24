import {
  AppShell,
  type AppShellAsideConfiguration,
  NavLink,
  Burger,
  Title,
  Stack,
  Group,
} from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { IconCalculator, IconCategory } from '@tabler/icons-react';
import { Link } from 'react-router';

type LayoutProps = {
  children: React.ReactNode;
  aside?: React.ReactNode;
  asideConfig?: AppShellAsideConfiguration;
};

function Layout({ children, aside, asideConfig }: LayoutProps) {
  const [opened, { toggle }] = useDisclosure();

  return (
    <AppShell
      header={{
        height: 60,
      }}
      navbar={{
        width: 250,
        breakpoint: 'sm',
        collapsed: {
          mobile: !opened,
        },
      }}
      aside={asideConfig}
      padding="md"
    >
      <AppShell.Header>
        <Group
          align="center"
          style={{
            height: 'inherit',
          }}
        >
          <Burger opened={opened} onClick={toggle} hiddenFrom="sm" size="sm" />
          <Title fz="h2">Renovation Calculator</Title>
        </Group>
      </AppShell.Header>
      <AppShell.Navbar>
        <NavLink
          component={Link}
          to="/"
          label="Калькулятор"
          leftSection={<IconCalculator size={32} />}
          styles={{
            label: {
              fontSize: '16pt',
            },
          }}
        />
        <NavLink
          component={Link}
          to="/catalog"
          label="Каталог"
          leftSection={<IconCategory size={32} />}
          styles={{
            label: {
              fontSize: '16pt',
            },
          }}
        />
      </AppShell.Navbar>
      <AppShell.Main>{children}</AppShell.Main>
      <AppShell.Aside>{aside}</AppShell.Aside>
    </AppShell>
  );
}

export default Layout;
