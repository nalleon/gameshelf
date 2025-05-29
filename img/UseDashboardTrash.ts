import axios from "axios";
import React, { useEffect, useState, useMemo } from "react";
import { useNavigate, useParams } from "react-router-dom";
import goback from '../assets/img/goback.png';
import gobackDM from '../assets/img/gobackDM.png';
import borrar from '../assets/img/ICON_ALIADAS/DELETE/DELETE_#37285f.png';
import borrarDM from '../assets/img/ICON_ALIADAS/DELETE/DELETE_WHITE.png';
import download from '../assets/img/ICON_ALIADAS/DOWNLOAD/DOWNLOAD_#37285f.png';
import downloadDM from '../assets/img/ICON_ALIADAS/DOWNLOAD/DOWNLOAD_WHITE.png';
import edit from '../assets/img/ICON_ALIADAS/EDIT/EDIT_#37285f.png';
import editDM from '../assets/img/ICON_ALIADAS/EDIT/EDIT_WHITE.png';
import questionIcon from "../assets/img/ICON_ALIADAS/FAQ/FAQ_#37285f.png";
import questionIconDM from "../assets/img/ICON_ALIADAS/FAQ/FAQ_WHITE.png";
import folderIcon from "../assets/img/ICON_ALIADAS/FOLDER/FOLDER-#37285f.png";
import folderIconDM from "../assets/img/ICON_ALIADAS/FOLDER/FOLDER_WHITE.png";
import moonIcon from "../assets/img/ICON_ALIADAS/MOON/MOON_WHITE.png";
import logoutIcon from "../assets/img/ICON_ALIADAS/SETTINGS/SETTINGS_#37285f.png";
import logoutIconDM from "../assets/img/ICON_ALIADAS/SETTINGS/SETTINGS_WHITE.png";
import sunIcon from "../assets/img/ICON_ALIADAS/SUN/SUN_#37285f.png";
import switchleft from "../assets/img/ICON_ALIADAS/SWITCH/SWITCH_LEFT.png";
import switchright from "../assets/img/ICON_ALIADAS/SWITCH/SWITCH_RIGHT.png";
import logo_dia from "../assets/img/logo_fondotransparente_horizontal_Mesa de trabajo 1_Mesa de trabajo 1_Mesa de trabajo 1.png";
import logo_noche from "../assets/img/logo_fondotransparente_horizontal_Mesa de trabajo 1_Mesa de trabajo 1_Mesa de trabajo 2.png";
import odpIcon from "../assets/img/ICON_ALIADAS/ODP/ODP_PURLPLE.png";
import odpIconDM from "../assets/img/ICON_ALIADAS/ODP/ODP_WHITE.png";
import restore from '../assets/img/ICON_ALIADAS/RESTORE/RESTORE_#37285f.png';
import restoreDM from '../assets/img/ICON_ALIADAS/RESTORE/RESTORE_WHITE.png';
import odsIcon from "../assets/img/ICON_ALIADAS/ODS/ODS_PRUPLE.png";
import odsIconDM from "../assets/img/ICON_ALIADAS/ODS/ODS_WHITE.png";
import odtIcon from "../assets/img/ICON_ALIADAS/ODT/ODT_PURPLE.png";
import odtIconDM from "../assets/img/ICON_ALIADAS/ODT/ODT_WHITE.png";

import pdfIcon from "../assets/img/ICON_ALIADAS/PDF/PDF_#37285f.png";
import pdfIconDM from "../assets/img/ICON_ALIADAS/PDF/PDF_WHITE.png";

import pictureIcon from "../assets/img/ICON_ALIADAS/PICTURE/PICTURE_#37285f.png";
import pictureIconDM from "../assets/img/ICON_ALIADAS/PICTURE/PICTURE_WHITE.png";

import docIcon from "../assets/img/ICON_ALIADAS/DOC/DOC_37285F.png";
import docIconDM from "../assets/img/ICON_ALIADAS/DOC/DOC_WHITE.png";

import xmlIcon from "../assets/img/ICON_ALIADAS/XML/XML_37285F.png";
import xmlIconDM from "../assets/img/ICON_ALIADAS/XML/XML_WHITE.png";

import { default as lupaIcon, default as lupaIconDM } from "../assets/img/lupa.png";
import dashboard from "../styles/dashboard.module.css";
import "../styles/global.css";
import { FileItem, FileWithFlag, FolderItem, FolderWithFlag, Item } from "../utils/Types";
import { URL_SERVER } from "../utils/Utils";
import { useTheme } from "../context/AppThemeContext";
import { Claims } from "../security/ProtectedRouteAdmin";
import { useJwt } from "react-jwt";
import secureLocalStorage from "react-secure-storage";


export const useDashboardTrash = () => {
 const [nameSearch, setNameSearch] = useState<string>("");
  const [files, setFiles] = useState<FileItem[]>([]);
  const [folders, setFolders] = useState<FolderItem[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [newFolderName, setNewFolderName] = useState("");
  const [showPolicyModal, setShowPolicyModal] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [showOptions, setShowOptions] = useState(false);
  const [viewMode, setViewMode] = useState<"list" | "grid">("list");
  const [openMenuKey, setOpenMenuKey] = useState<string | null>(null);
  const [showUploadFileModal, setShowUploadFileModal] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [showEditModal, setShowEditModal] = useState(false);
  const [editName, setEditName] = useState("");
  const [editItemId, setEditItemId] = useState<string | null>(null);
  const [editIsFolder, setEditIsFolder] = useState<boolean>(false);

  const navigate = useNavigate();
  const goToMainDashboard = () => navigate("/dashboard");
  const goToAdmin = () => {
    navigate("/admin");
    navigate(0);
  };

  const { isNight, toggleNightMode } = useTheme();

  const logoActual = isNight ? logo_noche : logo_dia;
  const switchRightActual = isNight ? switchright : switchleft;
  const moonIconActual = isNight ? moonIcon : sunIcon;
  const lupaActual = isNight ? lupaIconDM : lupaIcon;
  const questionActual = isNight ? questionIconDM : questionIcon;
  const logoutActual = isNight ? logoutIconDM : logoutIcon;
  const borrarActual = isNight ? borrarDM : borrar;
  const restoreActual = isNight ? restoreDM : restore;
  const goBackActual = isNight? gobackDM : goback;
  const folderActual = isNight ? folderIconDM : folderIcon;
  const pdfActual = pdfIcon;
  const odtActual = odtIcon;
  const odsActual = odsIcon;
  const odpActual = odpIcon;
  const docActual = docIcon;
  const xmlActual = xmlIcon;
  const pictureActual = pictureIcon;
  const questionMosaic = questionIcon;

  const storageToken = secureLocalStorage.getItem("token");
  const token = typeof storageToken === "string" ? storageToken : null;
  const { decodedToken } = useJwt<Claims>(token || "");
  const isAdmin = decodedToken?.role.name === "ROLE_ADMIN";

  useEffect(() => {
    setNameSearch("");
    fetchData();
  }, []);

  const fetchData = async (): Promise<void> => {
    try {
      const [filesResp, foldersResp] = await Promise.all([
        axios.get(`${URL_SERVER}/v2/files/trashed`, {
          headers: { Authorization: `Bearer ${token}` },
        }),
        axios.get(`${URL_SERVER}/v2/folders/trashed`, {
          headers: { Authorization: `Bearer ${token}` },
        }),
      ]);

      setFiles(filesResp.data.data.map((f: any) => ({
        id: String(f.id),
        name: String(f.name),
        type: String(f.type),
        creation_date: f.creation_date,
        last_update_date: f.last_update_date,
      })));

      setFolders(foldersResp.data.data.map((f: any) => ({
        id: String(f.id),
        name: String(f.name),
        creation_date: f.creation_date,
        last_update_date: f.last_update_date,
      })));
    } catch (err) {
      console.error("Error al obtener datos:", err);
    }
  };

  const fetchDataFiltered = async (term: string): Promise<void> => {
    try {
      const [filesResp, foldersResp] = await Promise.all([
        axios.get(`${URL_SERVER}/v2/files/trashed/names/{name}?q=${term}`, {
          headers: { Authorization: `Bearer ${token}` },
        }),
        axios.get(`${URL_SERVER}/v2/folders/trashed/names/{name}?q=${term}`, {
          headers: { Authorization: `Bearer ${token}` },
        }),
      ]);

      setFiles(filesResp.data.data.map((f: any) => ({
        id: String(f.id),
        name: String(f.name),
        type: String(f.type),
        creation_date: f.creation_date,
        last_update_date: f.last_update_date,
      })));

      setFolders(foldersResp.data.data.map((f: any) => ({
        id: String(f.id),
        name: String(f.name),
        creation_date: f.creation_date,
        last_update_date: f.last_update_date,
      })));
    } catch (err) {
      console.error("Error al obtener datos:", err);
    }
  };

  const getFileIcon = (type: string): string => {
    if (type === "application/pdf") return pdfActual;
    if (type === "application/vnd.oasis.opendocument.text") return odtActual;
    if (type === "application/vnd.oasis.opendocument.spreadsheet") return odsActual;
    if (type === "application/vnd.oasis.opendocument.presentation") return odpActual;
    if (type === "application/vnd.openxmlformats-officedocument.wordprocessingml.document") return docActual;
    if (type === "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet") return xmlActual;
    if (type === "text/plain") return docActual;
    if (type.startsWith("image/")) return pictureActual;
    return questionMosaic;
  };

  const allItems: Item[] = useMemo(() => [
    ...folders.map(folder => ({ ...folder, isFolder: true as const })),
    ...files.map(file => ({ ...file, isFolder: false as const })),
  ], [folders, files]);


  const toggleItemMenu = (key: string) => {
    setOpenMenuKey(prev => (prev === key ? null : key));
  };

  const handleDelete = async (key: string, isFolder: boolean) => {
    try {
      await axios.delete(`${URL_SERVER}/v2/${isFolder ? 'folders' : 'files'}/${key}/force`, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });
      await fetchData();
      setOpenMenuKey(null);
    } catch (err) {
      console.error("Error al eliminar archivo:", err);
    }
  };

  const handleRestore = async (key: string, isFolder: boolean) => {
    try {
      await axios.post(`${URL_SERVER}/v2/${isFolder ? 'folders' : 'files'}/${key}/restore`, null, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });
      await fetchData();
      setOpenMenuKey(null);
    } catch (err) {
      console.error("Error al restaurar:", err);
    }
  };

    /**
   * UseEffects
   */
  useEffect(() => {
    setNameSearch("");
    fetchData();
  }, []);

  return {
    // estados
    nameSearch, setNameSearch,
    files, folders,
    showModal, setShowModal,
    newFolderName, setNewFolderName,
    showPolicyModal, setShowPolicyModal,
    sidebarOpen, setSidebarOpen,
    showOptions, setShowOptions,
    viewMode, setViewMode,
    openMenuKey, setOpenMenuKey,
    showUploadFileModal, setShowUploadFileModal,
    selectedFile, setSelectedFile,
    showEditModal, setShowEditModal,
    editName, setEditName,
    editItemId, setEditItemId,
    editIsFolder, setEditIsFolder,
    // navegación
    goToMainDashboard,
    goToAdmin,
    // tema
    isNight,
    toggleNightMode,
    icons: {
      logoActual,
      switchRightActual,
      moonIconActual,
      lupaActual,
      questionActual,
      logoutActual,
      borrarActual,
      restoreActual,
      goBackActual,
      folderActual
    },
    // funciones
    getFileIcon,
    allItems,
    fetchData,
    fetchDataFiltered,
    toggleItemMenu,
    handleDelete,
    handleRestore,
    isAdmin,
    token,
    navigate
  };
};
export default useDashboardTrash;