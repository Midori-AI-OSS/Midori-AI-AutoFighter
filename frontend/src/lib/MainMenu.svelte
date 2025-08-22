<script>
  import { Play, Users, User, Settings, Package, PackageOpen, Hammer, MessageSquare } from 'lucide-svelte';
  export let run = () => {};
  export let party = () => {};
  export let edit = () => {};
  export let pulls = () => {};
  export let craft = () => {};
  export let settings = () => {};
  export let feedback = () => {};
  export let inventory = () => {};
  export let battleActive = false;
  export let items = [];
  $: items = [
    { icon: Play, label: 'Run', action: run, disabled: false },
    { icon: Users, label: 'Party', action: party, disabled: battleActive },
    { icon: User, label: 'Edit', action: edit, disabled: battleActive },
    { icon: PackageOpen, label: 'Pulls', action: pulls, disabled: battleActive },
    { icon: Hammer, label: 'Craft', action: craft, disabled: battleActive },
    { icon: Settings, label: 'Settings', action: settings, disabled: false },
    { icon: MessageSquare, label: 'Feedback', action: feedback, disabled: false },
    { icon: Package, label: 'Inventory', action: inventory, disabled: battleActive }
  ];
</script>

<!-- No visual output; this component only prepares the menu item array. -->
