package es.gameshelf.domain;

import java.util.Date;
import java.util.Objects;

/**
 * @author Nabil L. A. @nalleon
 */
public class GameCollectionItem {
    /**
     * Properties
     */
    private int id;
    private Game game;
    private Collection collection;
    private Format format;
    private Platform platform;
    private Edition edition;
    private Region region;
    private Date additionDate;
    /**
     * Default constructor of the class
     */
    public GameCollectionItem() {
    }

    /**
     * Constructor of the class
     * @param id of the GameCollectionItemEntity
     */
    public GameCollectionItem(int id) {
        this.id = id;
    }

    /**
     * Full constructor of the class
     * @param id of the GameCollectionItemEntity
     * @param game of the GameCollectionItemEntity
     * @param collection of the GameCollectionItemEntity
     * @param format of the GameCollectionItemEntity
     * @param platform of the GameCollectionItemEntity
     * @param edition of the GameCollectionItemEntity
     * @param region of the GameCollectionItemEntity
     * @param additionDate  of the GameCollectionItemEntity
     */
    public GameCollectionItem(int id, Game game, Collection collection, Format format, Platform platform, Edition edition,
                              Region region, Date additionDate) {
        this.id = id;
        this.game = game;
        this.collection = collection;
        this.format = format;
        this.platform = platform;
        this.edition = edition;
        this.region = region;
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

    public Game getGame() {
        return game;
    }

    public void setGame(Game game) {
        this.game = game;
    }

    public Collection getCollection() {
        return collection;
    }

    public void setCollection(Collection collection) {
        this.collection = collection;
    }

    public Format getFormat() {
        return format;
    }

    public void setFormat(Format format) {
        this.format = format;
    }

    public Platform getPlatform() {
        return platform;
    }

    public void setPlatform(Platform platform) {
        this.platform = platform;
    }

    public Edition getEdition() {
        return edition;
    }

    public void setEdition(Edition edition) {
        this.edition = edition;
    }

    public Region getRegion() {
        return region;
    }

    public void setRegion(Region region) {
        this.region = region;
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
        GameCollectionItem that = (GameCollectionItem) o;
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
                ", game=" + game +
                ", collection=" + collection +
                ", format=" + format +
                ", platform=" + platform +
                ", edition=" + edition +
                ", region=" + region +
                ", additionDate=" + additionDate +
                '}';
    }
}
