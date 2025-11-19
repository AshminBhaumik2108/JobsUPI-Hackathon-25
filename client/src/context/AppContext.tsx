import { createContext, useContext, useState, ReactNode } from "react";

export type SeekerProfile = {
  _id?: string;
  name?: string;
  contact?: string;
  location?: string;
  skills: string[];
  interests: string[];
  personality: string[];
};

export type AppContextValue = {
  profile: SeekerProfile;
  setProfile: (profile: SeekerProfile) => void;
  isProfileSaved: boolean;
  setIsProfileSaved: (value: boolean) => void;
  selectedRoleId?: string;
  setSelectedRoleId: (id?: string) => void;
  roleInsight?: string;
  setRoleInsight: (value?: string) => void;
};

const defaultProfile: SeekerProfile = {
  skills: [],
  interests: [],
  personality: []
};

const AppContext = createContext<AppContextValue | null>(null);

export const AppProvider = ({ children }: { children: ReactNode }) => {
  const [profile, setProfile] = useState<SeekerProfile>(defaultProfile);
  const [isProfileSaved, setIsProfileSaved] = useState(false);
  const [selectedRoleId, setSelectedRoleId] = useState<string | undefined>();
  const [roleInsight, setRoleInsight] = useState<string | undefined>();

  return (
    <AppContext.Provider value={{ profile, setProfile, isProfileSaved, setIsProfileSaved, selectedRoleId, setSelectedRoleId, roleInsight, setRoleInsight }}>
      {children}
    </AppContext.Provider>
  );
};

export const useAppContext = () => {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error("useAppContext must be used within AppProvider");
  return ctx;
};
