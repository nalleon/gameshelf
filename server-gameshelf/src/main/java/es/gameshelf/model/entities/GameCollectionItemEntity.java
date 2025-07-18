package es.gameshelf.model.entities;

import java.util.Date;
import java.util.Objects;

/**
 * @author Nabil L. A. @nalleon
 */
public class GameCollectionItemEntity {
    /**
     * Properties
     */
    private int id;
    private GameEntity gameEntity;
    private CollectionEntity collectionEntity;
    private FormatEntity formatEntity;
    private PlatformEntity platformEntity;
    private EditionEntity editionEntity;
    private RegionEntity regionEntity;
    private Date additionDate;
    /**
     * Default constructor of the class
     */
    public GameCollectionItemEntity() {
    }

    /**
     * Constructor of the class
     * @param id of the GameCollectionItemEntity
     */
    public GameCollectionItemEntity(int id) {
        this.id = id;
    }

    /**
     * Full constructor of the class
     * @param id of the GameCollectionItemEntity
     * @param gameEntity of the GameCollectionItemEntity
     * @param collectionEntity of the GameCollectionItemEntity
     * @param formatEntity of the GameCollectionItemEntity
     * @param platformEntity of the GameCollectionItemEntity
     * @param editionEntity of the GameCollectionItemEntity
     * @param regionEntity of the GameCollectionItemEntity
     * @param additionDate  of the GameCollectionItemEntity
     */
    public GameCollectionItemEntity(int id, GameEntity gameEntity, CollectionEntity collectionEntity, FormatEntity formatEntity, PlatformEntity platformEntity, EditionEntity editionEntity,
                                    RegionEntity regionEntity, Date additionDate) {
        this.id = id;
        this.gameEntity = gameEntity;
        this.collectionEntity = collectionEntity;
        this.formatEntity = formatEntity;
        this.platformEntity = platformEntity;
        this.editionEntity = editionEntity;
        this.regionEntity = regionEntity;
        this.additionDate = additionDate;
    }

    /**
     * Getters and setters
     */
    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public GameEntity getGame() {
        return gameEntity;
    }

    public void setGame(GameEntity gameEntity) {
        this.gameEntity = gameEntity;
    }

    public CollectionEntity getCollection() {
        return collectionEntity;
    }

    public void setCollection(CollectionEntity collectionEntity) {
        this.collectionEntity = collectionEntity;
    }

    public FormatEntity getFormat() {
        return formatEntity;
    }

    public void setFormat(FormatEntity formatEntity) {
        this.formatEntity = formatEntity;
    }

    public PlatformEntity getPlatform() {
        return platformEntity;
    }

    public void setPlatform(PlatformEntity platformEntity) {
        this.platformEntity = platformEntity;
    }

    public EditionEntity getEdition() {
        return editionEntity;
    }

    public void setEdition(EditionEntity editionEntity) {
        this.editionEntity = editionEntity;
    }

    public RegionEntity getRegion() {
        return regionEntity;
    }

    public void setRegion(RegionEntity regionEntity) {
        this.regionEntity = regionEntity;
    }

    public Date getAdditionDate() {
        return additionDate;
    }

    public void setAdditionDate(Date additionDate) {
        this.additionDate = additionDate;
    }

    @Override
    public boolean equals(Object o) {
        if (o == null || getClass() != o.getClass()) return false;
        GameCollectionItemEntity that = (GameCollectionItemEntity) o;
        return id == that.id;
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(id);
    }

    @Override
    public String toString() {
        return "GameCollectionItemEntity{" +
                "id=" + id +
                ", gameEntity=" + gameEntity +
                ", collectionEntity=" + collectionEntity +
                ", formatEntity=" + formatEntity +
                ", platformEntity=" + platformEntity +
                ", editionEntity=" + editionEntity +
                ", regionEntity=" + regionEntity +
                ", additionDate=" + additionDate +
                '}';
    }
}
