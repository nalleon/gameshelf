package es.gameshelf.model.entities;

import java.util.Date;
import java.util.Objects;

public class WishListItemEntity {
    /**
     * Properties
     */
    private int id;
    private int priority;
    private Date additionDate;
    private String annotation;
    private FormatEntity formatEntity;
    private PlatformEntity platformEntity;
    private EditionEntity editionEntity;
    private RegionEntity regionEntity;
    private GameEntity gameEntity;
    private UserEntity userEntity;

    /**
     * Default constructor of the class
     */
    public WishListItemEntity() {
    }

    /**
     * Constructor of the class
     * @param id of the wishlist item
     */
    public WishListItemEntity(int id) {
        this.id = id;
    }

    /**
     * Full constructor of the class
     * @param id of the wishlist item
     * @param priority of the wishlist item
     * @param additionDate of the wishlist item
     * @param annotation of the wishlist item
     * @param formatEntity of the wishlist item
     * @param platformEntity of the wishlist item
     * @param editionEntity of the wishlist item
     * @param regionEntity of the wishlist item
     * @param gameEntity of the wishlist item
     * @param userEntity of the wishlist item
     */
    public WishListItemEntity(int id, int priority, Date additionDate, String annotation, FormatEntity formatEntity, PlatformEntity platformEntity,
                              EditionEntity editionEntity, RegionEntity regionEntity, GameEntity gameEntity, UserEntity userEntity) {
        this.id = id;
        this.priority = priority;
        this.additionDate = additionDate;
        this.annotation = annotation;
        this.formatEntity = formatEntity;
        this.platformEntity = platformEntity;
        this.editionEntity = editionEntity;
        this.regionEntity = regionEntity;
        this.gameEntity = gameEntity;
        this.userEntity = userEntity;
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

    public int getPriority() {
        return priority;
    }

    public void setPriority(int priority) {
        this.priority = priority;
    }

    public Date getAdditionDate() {
        return additionDate;
    }

    public void setAdditionDate(Date additionDate) {
        this.additionDate = additionDate;
    }

    public String getAnnotation() {
        return annotation;
    }

    public void setAnnotation(String annotation) {
        this.annotation = annotation;
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

    public GameEntity getGame() {
        return gameEntity;
    }

    public void setGame(GameEntity gameEntity) {
        this.gameEntity = gameEntity;
    }

    public UserEntity getUser() {
        return userEntity;
    }

    public void setUser(UserEntity userEntity) {
        this.userEntity = userEntity;
    }

    @Override
    public boolean equals(Object o) {
        if (o == null || getClass() != o.getClass()) return false;
        WishListItemEntity that = (WishListItemEntity) o;
        return id == that.id;
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(id);
    }

    @Override
    public String toString() {
        return "WishListItemEntity{" +
                "id=" + id +
                ", priority=" + priority +
                ", additionDate=" + additionDate +
                ", annotation='" + annotation + '\'' +
                ", formatEntity=" + formatEntity +
                ", platformEntity=" + platformEntity +
                ", editionEntity=" + editionEntity +
                ", regionEntity=" + regionEntity +
                ", gameEntity=" + gameEntity +
                ", userEntity=" + userEntity +
                '}';
    }
}
