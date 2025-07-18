package es.gameshelf.domain;

import java.util.Date;
import java.util.Objects;

public class WishListItem {
    /**
     * Properties
     */
    private int id;
    private int priority;
    private Date additionDate;
    private String annotation;
    private Format format;
    private Platform platform;
    private Edition edition;
    private Region region;
    private Game game;
    private User user;

    /**
     * Default constructor of the class
     */
    public WishListItem() {
    }

    /**
     * Constructor of the class
     * @param id of the wishlist item
     */
    public WishListItem(int id) {
        this.id = id;
    }

    /**
     * Full constructor of the class
     * @param id of the wishlist item
     * @param priority of the wishlist item
     * @param additionDate of the wishlist item
     * @param annotation of the wishlist item
     * @param format of the wishlist item
     * @param platform of the wishlist item
     * @param edition of the wishlist item
     * @param region of the wishlist item
     * @param game of the wishlist item
     * @param user of the wishlist item
     */
    public WishListItem(int id, int priority, Date additionDate, String annotation, Format format, Platform platform,
                        Edition edition, Region region, Game game, User user) {
        this.id = id;
        this.priority = priority;
        this.additionDate = additionDate;
        this.annotation = annotation;
        this.format = format;
        this.platform = platform;
        this.edition = edition;
        this.region = region;
        this.game = game;
        this.user = user;
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

    public Game getGame() {
        return game;
    }

    public void setGame(Game game) {
        this.game = game;
    }

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }

    @Override
    public boolean equals(Object o) {
        if (o == null || getClass() != o.getClass()) return false;
        WishListItem that = (WishListItem) o;
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
                ", format=" + format +
                ", platform=" + platform +
                ", edition=" + edition +
                ", region=" + region +
                ", game=" + game +
                ", user=" + user +
                '}';
    }
}
